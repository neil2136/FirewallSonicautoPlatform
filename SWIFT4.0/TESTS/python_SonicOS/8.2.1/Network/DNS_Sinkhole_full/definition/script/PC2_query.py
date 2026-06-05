import subprocess
import sys


domains = sys.argv[1]
domain_list = domains.strip('[]').replace(' ', '').split(',')
# print(domain_list)

try:
    for domain in domain_list:
        # print(domain)
        domain = domain.strip().replace(r'\n', '')
        c=subprocess.Popen(["dig", "+short", "+retry=0", domain], stdout=subprocess.PIPE)
        # print(c.communicate()[0])
finally:
    print("...... Query END")
