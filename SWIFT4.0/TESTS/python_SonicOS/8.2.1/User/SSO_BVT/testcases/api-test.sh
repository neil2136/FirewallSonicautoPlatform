#! /bin/sh

# Script to send SSO REST API user login/logout request to a SonicWall.
#
# Usage is:
#
#   To log in a single user:
#        api-test.sh [--json] post
# 
#   To log in multiple users:
#        api-test.sh [--json] post-multi
# 
#   To log out a single user:
#        api-test.sh [--json] delete
# 
#   To log out a single user with the user name included in the request data:
#        api-test.sh [--json] delete-with-name
# 
#   To log out multiple users:
#        api-test.sh [--json] delete-multi
#
# By default it will send XML. Add the "--json" argument to send JSON.
#
# With no arguments it will log in a single user sending XML:
#      api-test.sh
#
# To change what is sent, edit the source XML/JSON files:
#
#  test.xml         - XML for single user add and delete-with-name.
#  test-multi.xml   - XML for multi user add and delete.
#  test.json        - JSON for single user add and delete-with-name.
#  test-multi.json  - JSON for multi user add and delete.
#
# Note: for single user delete-with-name and multi user delete it sends the same
# data as for an add. This is more than is needed for deletes but the extra data
# sent is ignored by the firewall.

function ReportUsage()
{
	echo ""
	echo "Usage:"
	echo "  api-test.sh [options] [request-type]"
	echo ""
	echo "Sends an SSO-API request to a SonicWall."
	echo ""
	echo "request-type is one of:"
	echo "  post              Post a single-user login from test.(xml|json)"
	echo "  post-multi        Post a multi-user login from test-multi.(xml|json)"
	echo "  delete            Send a single-user logout with no data"
	echo "  delete-with-name  Send a single-user logout, data from test.(xml|json)"
	echo "  delete-multi      Send a multi-user logout, data from test-multi.(xml|json)"
	echo ""
	echo "If no request-type is given then the default is post."
	echo ""
	echo "Options:"
	echo "  -x, --xml               Send the request data in XML format (the default)"
	echo "  -j, --json              Send the request data in JSON format"
	echo "  -f, --firewall <ip>     The firewall IP address, optionally with ':<port>'"
	echo "  -s, --secret <secret>   The shared secret"
	echo "  -a, --auth-level <lvl>  Authentication level (low, medium, high or high-512)"
	echo "  -c, --csrf-prevent      Use CSRF prevention"
	echo "  -C, --cert <cert-file> <key-file>"
	echo "                          Use a certfificate. The certificate/key files must be"
	echo "                          given as a full path (use './<file>' if local)."
	echo "  -q, --quiet             Report only failures."
	echo "  -v, --verbose           Be verbose."
	echo "  -V, --very-verbose      Be more verbose (including verbose output from curl)."
	echo "  -T, --verbose+trace     Be more verbose (including trace output from curl)."
	echo "  -h, --help              Display this help and exit."
}


SNWL='192.168.168.168'
SECRET='1234'
TYPE="json"
AUTH_LEVEL="low"
CSRF="Yes"
CERT_FILE=
KEY_FILE=
QUIET="No"
VERBOSE="No"
VRB_ARG=""
while (test "${1:0:1}" == "-") do
	case $1 in
		-x|--xml)			TYPE=xml;;
		-j|--json)			TYPE=json;;
		-f|--firewall)		SNWL=$2; shift;;
		-s|--secret)		SECRET=$2; shift;;
		-a|--auth-level)	AUTH_LEVEL=$2; shift;;
		-c|--csrf-prevent)	CSRF=Yes;;
		-C|--cert)			CERT_FILE=$2; KEY_FILE=$3; shift; shift;;
		-q|--quiet)			QUIET="Yes";;
		-v|--verbose)		VERBOSE="Yes";;
		-V|--very-verbose)	VERBOSE="Very"; VRB_ARG="--verbose";;
		-T|--verbose+trace)	VERBOSE="Very"; VRB_ARG="--trace -";;
		-h|--help)
			ReportUsage;
			if (test $SHLVL -eq 1) then return; else exit; fi
			;;
		*)	echo "Unknown option: $1"
			ReportUsage;
			if (test $SHLVL -eq 1) then return; else exit; fi
			;;
	esac
	shift
done

TEST="$1"
if (test "$TEST" == "") then
	TEST="post"
fi

DATA_FILE=
RQST_ARG=
URI_SUFFIX=

case $TEST in
	post)
		DATA_FILE="test.$TYPE"
		;;
	post-multi)
		DATA_FILE="test-multi.$TYPE"
		;;
	delete)
		RQST_ARG="--request DELETE"
		URI_SUFFIX="/192.168.168.99"
		;;
	delete-with-name)
		RQST_ARG="--request DELETE"
		DATA_FILE="test.$TYPE"
		URI_SUFFIX="/192.168.168.99"
		;;
	delete-multi)
		RQST_ARG="--request DELETE"
		DATA_FILE="test-multi.$TYPE"
		URI_SUFFIX="/multi"
		;;
	*)
		echo "Invalid test '$TEST'"
		if (test $SHLVL -eq 1) then return; else exit; fi
esac

FINISHED="No"
RETRIES=0
while [ $FINISHED == "No" ]; do
	#===============================================================
	#
	# Authenticator calculation:
	#
	#
	# The authenticator is 64 bytes for SHA256, 128 bytes for SHA512:
	#  - a 4-byte flags field,
	#  - a 4-byte sequence number field (used only if using CSRF prevention),
	#  - a random number, 24 bytes for SHA256, 56-bytes for SHA512,
	#  - a 32-byte SHA256 or 64-byte SHA512 hash of:
	#      - the flags, sequence number and random number,
	#      - the shared secret,
	#      - the request content, or the URI if no content.

	# First the flags and sequence number, 4 bytes each:
	# (flags set to 1 means that we want to get back a reply authenticator)
	RQST_FLAGS="00000001"
	RQST_SEQNO=0
	if (test "$CSRF" == "Yes") then
		if [ ! -f api.seq ]; then
			echo -n "1" >api.seq
		fi
		RQST_SEQNO=$(cat api.seq)
		echo -n $(expr $RQST_SEQNO + 1) >api.seq
	fi
	echo -n $RQST_FLAGS | xxd -r -p >sha.in
	printf "%08x" $RQST_SEQNO | xxd -r -p >>sha.in

	if (test "$AUTH_LEVEL" == "high-512") then
		# Generate and add a 56-byte random number:
		head -c 56 </dev/random >>sha.in
		DIGEST_LEN=64
		RAND_LEN=56
		SHASUM=sha512sum
	else
		if (test "$AUTH_LEVEL" == "high") then
			# Generate and add a 24-byte random number:
			head -c 24 </dev/random >>sha.in
		else
			# Medium level: generate and add a predictable 24-byte not-so-random number:
			echo "0102030405060708090a0b0c0d0e0f101112131415161718" | xxd -r -p >>sha.in
		fi
		DIGEST_LEN=32
		RAND_LEN=24
		SHASUM=sha256sum
	fi

	# Add the secret and, for high level, the body content or URI:
	echo -n "$SECRET" >>sha.in
	if (test "${AUTH_LEVEL:0:4}" == "high" ) then
		if (test "$DATA_FILE" != "") then
			cat $DATA_FILE >>sha.in
		else
			echo -n "api/sso/user$URI_SUFFIX" >>sha.in
		fi
	fi 

	# We now set up the authenticator in auth.bin. It begins with the flags, sequence
	# number and random number (32 bytes total for SHA256, 64 bytes total for SHA256)
	# which we can extract from the start of the SHA input in sha.in. Then we append
	# to that the 32-byte SHA256 or 64-byte SHA512 hash of the input data in sha.in.
	# And then finally the whole thing needs to be base64 encoded.
	head -c $DIGEST_LEN sha.in >auth.bin
	$SHASUM sha.in | sed 's/ .*//' | xxd -r -p >>auth.bin
	AUTH=$(base64 -w 0 auth.bin)

	if (test "$VERBOSE" != "No") then
		if (test "$VERBOSE" == "Very") then
			echo "$SHASUM input:"
			xxd -p -c 32 sha.in
		fi
		echo "Flags: `head -c 4 auth.bin | xxd -p`"
		echo "SeqNo: `head -c 8 auth.bin | tail -c 4 | xxd -p`"
		echo "Rand:  `head -c $(expr $RAND_LEN + 8) auth.bin | tail -c $RAND_LEN | xxd -p -c 100`"
		echo "Hash:  `tail -c $DIGEST_LEN auth.bin | xxd -p -c 100`"
	fi

	#===============================================================


	CERT_ARGS=
	if (test "$CERT_FILE" != "") then
		CERT_ARGS="--cert $CERT_FILE --key $KEY_FILE"
	fi

	DATA_ARG=
	if (test "$DATA_FILE" != "") then
		DATA_ARG="--data-binary @$DATA_FILE"
	fi 

	if (test "$QUIET" == "No") then
		echo "curl $RQST_ARG $DATA_ARG $VRB_ARG --header \"Authorization: SNWL-API-Auth $AUTH\" --header \"Content-Type: application/$TYPE\" --header \"Accept: application/$TYPE\" -k https://$SNWL/api/sso/user$URI_SUFFIX $CERT_ARGS -i -s"
	fi
	curl $RQST_ARG $DATA_ARG $VRB_ARG --header "Authorization: SNWL-API-Auth $AUTH" --header "Content-Type: application/$TYPE" --header "Accept: application/$TYPE" -k https://$SNWL/api/sso/user$URI_SUFFIX $CERT_ARGS -i -s >curl.out

	SHOW_RESP="Yes"
	if (test "$QUIET" == "Yes") then
		if ( grep -q "^HTTP/1.. 200 OK" curl.out ); then
			SHOW_RESP="No"
		fi
	fi
	if (test "$SHOW_RESP" == "Yes") then
		echo ""
		echo "Response from $SNWL:"
		cat curl.out
	fi

	FINISHED="Yes"

	grep "Authorization: SNWL-API-Auth" curl.out | awk '{ print $3 }' | base64 -di >rauth.bin

	if [ -s rauth.bin ]; then
		# Reply authenticator is an n-byte random number + n-byte SHA hash of the
		# 64-byte (SHA256) or 128-byte (SHA512) request authenticator, the random
		# number and the shared secret (where n is 32 for SHA256, 64 for SHA512).
		cp auth.bin rsha.in
		head -c $DIGEST_LEN rauth.bin >>rsha.in
		echo -n "$SECRET" >>rsha.in
		$SHASUM rsha.in | sed 's/ .*//' | xxd -r -p >xpct.bin
		tail -c $DIGEST_LEN rauth.bin >rhash.bin

		if ( diff -q rhash.bin xpct.bin &>/dev/null ); then
			if (test "$QUIET" == "No") then
				echo Response authenticator is correct

				if (test "$CSRF" == "Yes") then
					if ( head -n 1 curl.out | grep -q "401 Unauthorized" && 
						 grep -q "WWW-Authenticate: SNWL-API-Auth Reset:" curl.out ); then
						# The sequence number check failed in the SonicWall and it has
						# generated a new sequence number to retry with, returning it as:
						#    "WWW-Authenticate: SNWL-API-Auth Reset:<new-seq-no>"
						grep "WWW-Authenticate:" curl.out | awk -F : '{ printf "%d", $3 }' >api.seq

						# Retry with the new sequence number once only
						if [ $RETRIES -eq 0 ]; then
							echo ""
							echo ""
							echo "A sequence number reset was returned, retrying..."
							echo ""
							let RETRIES=RETRIES+1
							FINISHED="No"
						fi
					fi
				fi
			fi
			rm *.in *.out *.bin
		else
			echo "Error: Response authenticator is not as expected!"
		fi 
	else
		echo "Error: No response authenticator in the reply!"
	fi
done

