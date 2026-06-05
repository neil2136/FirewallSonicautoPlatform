import re
import os
import time,datetime
from sqlalchemy import or_, and_
from urllib import parse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from runner.utils.models import User, Platform, Product,TestSuite, TestBed, JobRequest, TestResult, ApTestSessionGroup, TestFailure, FailureType, CoreDumpDetail,AIO
from runner.settings import Params, get_sonicauto_session, LOGGING

logger = LOGGING.getLogger(__name__)


class SonicAuto:
    default_args = {
        'g_cc': '',
        'g_scmlabel': '',
        'g_testbed': '',
        'g_avt_mountpoint': '',
        'g_build': '',
        'g_product': '',
        'g_user': '',
        'g_requesttime': '',
        'mount_point': '',
        'g_qbs': '',
        'g_resource': '',
        'bundle': '',
        'rgname': '',
        'log_level': '',
        'log_dir': ''
    }

    def __init__(self):
        if Params.database_host:
            sonicauto_conn = f"postgres://sonicauto:%s@{Params.database_host}:5432/sonicauto" % parse.quote('s0nicw@ll')
            self.session =  sessionmaker(bind=create_engine(sonicauto_conn))()
        else:
            self.session = get_sonicauto_session()
            
    def get_session_group_name(self, scmlabel, productid):
        try:
            session_group = self.session.query(ApTestSessionGroup).filter(ApTestSessionGroup.scmlabel == scmlabel).filter(ApTestSessionGroup.productid == productid)
            return session_group[0].group_name
        except Exception as e:
            logger.error(f"Not able to get session group name for scmlabel {scmlabel} and productid {productid}")
            return ''

    def get_product_id_from_platform(self, platform):
        try:
            data = self.session.query(Platform).filter(Platform.alias == platform)
            return data[0].productid
        except Exception as e:
            logger.error(f"Not able to get product id from platform {platform}")
            return 0

    def get_product_name_from_product_id(self, product_id):
        try:
            data = self.session.query(Product).filter(Product.productid == product_id)
            return data[0].name
        except Exception as e:
            logger.error(f"Not able to get product name from product {product_id}")
            return ''

    def get_log_location_from_job_request(self, job_id):
        try:
            data = self.session.query(JobRequest).filter(JobRequest.qbsjobid == job_id).first()
            if data is not None:
                return data.log_location
            else:
                logger.warning(f"No log location found for job request with job_id {job_id}")
                return None
        except Exception as e:
            logger.error(f"Not able to get log location from job request {job_id}: {e}")
            return None
            
    def get_testsuite_details(self, pathname):
        for i in range(0,5):
            try:
                suites = self.session.query(TestSuite).filter(or_(TestSuite.path == Params.path, TestSuite.path == Params.path.replace('//depot/SQA','')))
                if Params.openstack and int(Params.openstack) == 1:
                    # topo = suites[-1].topology_definition
                    topo = Params.topology
                    if topo and topo != '':
                        if 'COMMON/data/topo' in topo:
                            topo_split=topo.split('COMMON/data/topo')
                            topo_url = 'https://gitlab.com/ssp3183542/swift4.0/COMMON/blob/master/data/topo' + topo_split[-1]
                        elif 'TESTS/SSLVPN' in topo:
                            topo_split=topo.split('TESTS/SSLVPN')
                            topo_url = 'https://gitlab.com/ssp3183542/swift4.0/tests_sub/sslvpn/blob/master' + topo_split[-1]
                        elif 'TESTS/EmailSecurity' in topo:
                            topo_split=topo.split('TESTS/EmailSecurity')
                            topo_url = 'https://gitlab.com/ssp3183542/swift4.0/tests_sub/emailsecurity/blob/master' + topo_split[-1]
                    else:
                        topo = 'No record'
                        topo_url = 'No record'
                    data = {
                        'testcases': suites[-1].testcases,
                        'exectime': suites[-1].exectime,
                        'display_name': suites[-1].display_name,
                        'topology_path':topo,
                        # 'topology_path':suites[-1].topology_definition,
                        'topology_link':topo_url
                        }
                else:
                    data = {
                        'testcases': suites[-1].testcases,
                        'exectime': suites[-1].exectime,
                        'display_name': suites[-1].display_name
                        }
            except Exception as e:
                logger.error(f"Not able to get test suite details for {pathname}: {e}")
                data = {
                    'testcases': 'No record',
                    'exectime': 'No record',
                    'display_name': pathname.replace('//depot/SQA','').split('/')[-1][:-3] 
                }
                if Params.rgname and re.search(r']',Params.rgname):
                    data['display_name'] = Params.rgname[Params.rgname.find(']')+1:]
                if Params.database_host:
                    sonicauto_conn = f"postgres://sonicauto:%s@{Params.database_host}:5432/sonicauto" % parse.unquote('s0nicw@ll')
                    self.session =  sessionmaker(create_engine(sonicauto_conn))()
                else:
                    logger.info('Rollback in function get_testsuite_details.')
                    self.session.rollback()
                    time.sleep(2)
                    self.session = get_sonicauto_session()                
        return data

    def get_testsuite_owner(self, pathname):
        try:
            suites = self.session.query(TestSuite).filter(or_(TestSuite.path == Params.path, TestSuite.path == Params.path.replace('//depot/SQA','')))
            users = self.session.query(User).filter(User.userid == suites[-1].ownerid)
            data = {
                'name': users[0].name
            }
            return data
        except Exception as e:
            logger.error(f"Not able to get test suite owner for {pathname}")
            return ''

    def get_testsuite_owner_via_rgname(self, rgname):
        display_name=rgname.split(']')[1]
        try:
            suites = self.session.query(TestSuite).filter(TestSuite.display_name == display_name)
            users = self.session.query(User).filter(User.userid == suites[-1].ownerid)
            data = {
                'name': users[0].name
            }
            return data
        except Exception as e:
            logger.error(f"Not able to get test suite owner for {rgname}")
            return ''

    def get_testsuite_owner_via_displayname(self, display_name):
        try:
            suites = self.session.query(TestSuite).filter(TestSuite.display_name == display_name)
            users = self.session.query(User).filter(User.userid == suites[-1].ownerid)
            return users[0].name
        except Exception as e:
            logger.error(f"Not able to get test suite owner for {display_name}")
            return ''      

    def get_full_name(self, username):
        try:
            users = self.session.query(User).filter(User.name == username)
            data = {
                'full_name': users[0].full_name
            }
            return data
        except Exception as e:
            logger.error("Not able to get full name for username {username}")
            data = {
                'full_name': 'root'
            }
            return data 

    def get_backup_owner(self, pathname):
        try:
            suites = self.session.query(TestSuite).filter(TestSuite.path == pathname)
            users = self.session.query(User).filter(User.userid == suites[-1].backup_ownerid)
            data = {
                'name': users[0].name
            }
            return data
        except Exception as e:
            logger.error(f"Not able to get backup owner for {pathname}")
            return ''

    def save_job_request_before_run(self):
        try:
            # Get userid
            users = self.session.query(User).filter(User.name == Params.user)

            # Get suiteid
            suites = self.session.query(TestSuite).filter(or_(TestSuite.path == Params.path, TestSuite.path == Params.path.replace('//depot/SQA','')))            # Get tbid
            testbeds = self.session.query(TestBed).filter(TestBed.name == Params.testbed)

            # Get platformid
            platforms = self.session.query(Platform).filter(Platform.alias == Params.product)

            # topology_id: not added at this moment7
            job_request = JobRequest()
            try:
                new_job_request = None
 #               new_job_request = self.session.query(JobRequest).filter(and_(not JobRequest.alpha_id, JobRequest.qbsjobid == Params.qbsjobid))
                new_job_request = self.session.query(JobRequest).filter(JobRequest.job_requestid == Params.qbsjobid)
                job_request=new_job_request[0]
                job_request.status = 'started'
            except:
                job_request = JobRequest()
                job_request.status = None
            try:
                job_request.topology_id = Params.openstack_tid
            except:
                pass
            job_request.qbsjobid = Params.qbsjobid
            job_request.jobname = Params.bundle
            job_request.qbs_serverid = Params.qbs
            job_request.requested_by = users[0].userid
            job_request.rerun_pass = 0
            job_request.rerun_fail = 0
            try:
                job_request.suiteid = suites[-1].testsuiteid
            except Exception as se:
                job_request.suiteid = None

            job_request.command = 'python3 ' + ' '.join(Params.command)
            job_request.platformid = platforms[0].platformid
            job_request.tbid = testbeds[0].tbid
            job_request.scmlabel = Params.scmlabel
            job_request.log_location = Params.server_log_location.strip('/')
            job_request.requested_time = Params.requesttime
            job_request.start_time = Params.starttime.strftime('%Y-%m-%d %H:%M:%S')
            job_request.build_file = Params.build
            try:
                if new_job_request[0] and Params.njs == 1:
                    self.session.commit()
            except:
                logger.info(job_request.job_requestid)
                self.session.add(job_request)
                self.session.commit()
                self.session.refresh(job_request)
            return job_request
        except Exception as e:
            logger.error(f"Not able to save job request before run with error {e.args}")
            logger.info(f'Rollback postgre.')
            self.session.rollback()
            return ''

    def save_job_request_after_run(self):
        try:
            new_job_request = None
 #               new_job_request = self.session.query(JobRequest).filter(and_(not JobRequest.alpha_id, JobRequest.qbsjobid == Params.qbsjobid))
            job_request = self.session.query(JobRequest).filter(JobRequest.qbsjobid == Params.qbsjobid).first()
            job_request.status = 'completed'
            job_request.rerun_pass = Params.rerun_pass
            job_request.rerun_fail = Params.rerun_fail
            try:
                self.session.commit()
                self.session.refresh()
            except Exception as e:
                pass
        except Exception as e:
            logger.error(f"Not able to save job request after run with error {e.args}")
            logger.info(f'Rollback postgre.')
            self.session.rollback()
            return ''
        return 'Save job request after run successfully'
        
    def save_result_before_run(self, results: list):
        job_requestid = ''
        job_request = self.save_job_request_before_run()
        if job_request:
            job_requestid = job_request.job_requestid
            logger.info('-------------')
            logger.info(job_requestid)
        if job_requestid == '':
            return job_requestid, 'Error: not able to create job_request record into database'

        if job_requestid == '':
            return 'Error: not able to create job_request record into database'
        else:
            additional_res={
                'platformid': '',
                'suiteid': '',
                'jobname': '',
            }
            try:
                additional_res['platformid']= job_request.platformid,
                additional_res['suiteid']= job_request.suiteid,
                additional_res['jobname']= job_request.jobname,
            except:
                pass
            i=0
            while i < len(results):
                tc = dict(results[i])
                tc['job_requestid'] = job_requestid
                self.save_test_case_result(res=tc,additional_res=additional_res)
                i += 1

        return job_requestid, 'Result got saved successfully'        
    
    def save_job_request(self):
        try:
            # Get userid
            users = self.session.query(User).filter(User.name == Params.user)

            # Get suiteid
            suites = self.session.query(TestSuite).filter(or_(TestSuite.path == Params.path, TestSuite.path == Params.path.replace('//depot/SQA','')))            # Get tbid
            testbeds = self.session.query(TestBed).filter(TestBed.name == Params.testbed)

            # Get platformid
            platforms = self.session.query(Platform).filter(Platform.alias == Params.product)

            # topology_id: not added at this moment7
            job_request = JobRequest()
            try:
                new_job_request = None
 #               new_job_request = self.session.query(JobRequest).filter(and_(not JobRequest.alpha_id, JobRequest.qbsjobid == Params.qbsjobid))
                new_job_request = self.session.query(JobRequest).filter(JobRequest.job_requestid == Params.qbsjobid)
                job_request=new_job_request[0]
                job_request.status = 'completed'
                logger.info('-------1')
            except:
                job_request = JobRequest()
                job_request.status = None
            try:
                job_request.topology_id = Params.openstack_tid
            except:
                pass
            job_request.qbsjobid = Params.qbsjobid
            job_request.jobname = Params.bundle
            job_request.qbs_serverid = Params.qbs
            job_request.requested_by = users[0].userid
            logger.info('-------2')

            try:
                job_request.suiteid = suites[-1].testsuiteid
            except Exception as se:
                job_request.suiteid = None

            job_request.command = 'python3 ' + ' '.join(Params.command)
            job_request.platformid = platforms[0].platformid
            job_request.tbid = testbeds[0].tbid
            job_request.scmlabel = Params.scmlabel
            job_request.log_location = Params.server_log_location.strip('/')
            job_request.requested_time = Params.requesttime
            job_request.start_time = Params.starttime
            job_request.build_file = Params.build
            try:
                if new_job_request[0] and Params.njs == 1:
                    self.session.commit()
            except:
                self.session.add(job_request)
                self.session.commit()
                self.session.refresh(job_request)
            return job_request
        except Exception as e:
            logger.error(f"Not able to save job request with error {e.args}")
            logger.info(f'Rollback postgre.')
            self.session.rollback()
            return ''

    def save_result(self, results: list):
        job_requestid = ''
        job_request = self.save_job_request()
        if job_request:
            job_requestid = job_request.job_requestid
            logger.info('-------------')
            logger.info(job_requestid)
        if job_requestid == '':
            return 'Error: not able to create job_request record into database'
        else:
            additional_res={
                'platformid': '',
                'suiteid': '',
                'jobname': '',
            }
            try:
                additional_res['platformid']= job_request.platformid,
                additional_res['suiteid']= job_request.suiteid,
                additional_res['jobname']= job_request.jobname,
            except:
                pass
            i=0
            while i < len(results):
                tc = dict(results[i])
                tc['job_requestid'] = job_requestid
                self.save_test_case_result(res=tc,additional_res=additional_res)
                i += 1

        return 'Result got saved successfully'

    def update_result(self, job_requestid, result):
        if job_requestid:
            logger.info('-------------')
            logger.info(job_requestid)
        if job_requestid == '':
            return 'Error: not able to get job_request record into database'
        else:
            result['job_requestid'] == job_requestid
            new_testresult = self.session.query(TestResult).filter(and_(TestResult.job_requestid == job_requestid,TestResult.filename == result['filename']))

        res=self.save_test_case_result(res=result)
        if res:
            return 'Result got saved successfully'
    
    def save_test_case_result(self, res={},additional_res={}):
        try:
            test_result = TestResult()
            try:
                new_testresult = None
                new_testresult = self.session.query(TestResult).filter(and_(TestResult.job_requestid == int(res['job_requestid']),TestResult.filename == res['filename']))
                test_result = new_testresult[0]
            except:
                test_result.matrixid = res['matrixid']
                test_result.parameters = res['parameters']
                test_result.scmlabel = res['scmlabel']
                test_result.alias = res['alias']
                test_result.product = 'SonicOS'
                test_result.suiteid = additional_res['suiteid']
                test_result.platformid = additional_res['platformid']
                test_result.jobname = additional_res['jobname']
            test_result.job_requestid = res['job_requestid']
            test_result.type = res['type']
            if res['title'] == '_FailedTest':
                res['title'] += '-unknown error, refer to stderr.log'
            test_result.title = res['title']
            test_result.result = res['result']
            test_result.starttime = res['starttime']
            test_result.endtime = res['endtime']
            test_result.filename = res['filename']
            test_result.log_link = res['log_link']
            test_result.uuid = res['uuid']
            #test_result.product = res['product']                
            try:
                diff =(datetime.datetime.strptime(test_result.endtime,"%Y-%m-%d %H:%M:%S.%f") -datetime.datetime.strptime(test_result.starttime,"%Y-%m-%d %H:%M:%S.%f")).seconds
                if diff<0:
                    diff = 300
                test_result.duration = diff
            except Exception as e:
                logger.info(e)
            try:
                product_id =self.get_product_id_from_platform(res['product'])
                product_name =self.get_product_name_from_product_id(product_id)
                test_result.product = product_name
            except:
                pass
            try:
                if new_testresult[0]:
                    self.session.commit()
            except:
                self.session.add(test_result)
                self.session.commit()
                self.session.refresh(test_result)
            if test_result.result == 'FAILED' or (test_result.result == 'SKIPPED' and res['dts_jira_link']):
                try:
                    users = self.session.query(User).filter(User.name == Params.user)
                    ftype = self.session.query(FailureType).filter(FailureType.name == res['ftype'])
                    test_faiure = TestFailure()
                    test_faiure.ftypeid = ftype[0].ftypeid
                    test_faiure.freason = res['ftype']
                    test_faiure.ownerid = users[0].userid
                    test_faiure.dtsid = None
                    test_faiure.jira = None
                    test_faiure.resultid = test_result.resultid
                    if res['dts_jira_link']:
                        dts = re.search(r'jobid=(\d+)', res['dts_jira_link'])
                        jira = re.search(r'sonicwall.atlassian.net/browse/(.+)', res['dts_jira_link'])
                        if dts:
                            test_faiure.dtsid = int(dts.group(1))
                        elif jira:
                            test_faiure.jira = jira.group(1)
                    self.session.add(test_faiure)
                    self.session.commit()
                    self.session.refresh(test_faiure)
                    return test_faiure.failureid
                except Exception as e:
                    logger.error(f"Not able to save test failure with error {e.args}")
                    return ''
            return test_result.resultid
        except Exception as e:
            logger.error(f"Not able to save test case result with error {e.args}")
            self.session.rollback()
            time.sleep(2)
            self.session = get_sonicauto_session()
            return ''
#winni
    def save_single_test_case_result(self, res={},additional_res={}):
        try:
            test_result = TestResult()
            test_result.matrixid = res['matrixid']
            test_result.job_requestid = res['job_requestid']
            test_result.type = res['type']
            test_result.title = res['title']
            test_result.parameters = res['parameters']
            test_result.alias = res['alias']
            test_result.result = res['result']
            test_result.starttime = res['starttime']
            test_result.endtime = res['endtime']
            test_result.filename = res['filename']
            test_result.log_link = res['log_link']
            test_result.uuid = res['uuid']
            test_result.scmlabel = res['scmlabel']
            #test_result.product = res['product']
            test_result.product = 'SonicOS'
            test_result.suiteid = additional_res['suiteid']
            test_result.platformid = additional_res['platformid']
            test_result.jobname = additional_res['jobname']

            try:
                diff =(datetime.datetime.strptime(test_result.endtime,"%Y-%m-%d %H:%M:%S.%f") -datetime.datetime.strptime(test_result.starttime,"%Y-%m-%d %H:%M:%S.%f")).seconds
                if diff<0:
                    diff = 300
                test_result.duration = diff
            except Exception as e:
                logger.info(e)
            try:
                product_id =self.get_product_id_from_platform(res['product'])
                product_name =self.get_product_name_from_product_id(product_id)
                test_result.product = product_name
            except:
                pass

            self.session.add(test_result)
            self.session.commit()
            self.session.refresh(test_result)
            if test_result.result == 'FAILED' or (test_result.result == 'SKIPPED' and res['dts_jira_link']):
                try:
                    users = self.session.query(User).filter(User.name == Params.user)
                    ftype = self.session.query(FailureType).filter(FailureType.name == res['ftype'])
                    test_faiure = TestFailure()
                    test_faiure.ftypeid = ftype[0].ftypeid
                    test_faiure.freason = res['ftype']
                    test_faiure.ownerid = users[0].userid
                    test_faiure.dtsid = None
                    test_faiure.jira = None
                    test_faiure.resultid = test_result.resultid
                    if res['dts_jira_link']:
                        dts = re.search(r'jobid=(\d+)', res['dts_jira_link'])
                        jira = re.search(r'sonicwall.atlassian.net/browse/(.+)', res['dts_jira_link'])
                        if dts:
                            test_faiure.dtsid = int(dts.group(1))
                        elif jira:
                            test_faiure.jira = jira.group(1)
                    self.session.add(test_faiure)
                    self.session.commit()
                    self.session.refresh(test_faiure)
                    return test_faiure.failureid
                except Exception as e:
                    logger.error(f"Not able to save test failure with error {e.args}")
                    return ''
            return test_result.resultid
        except Exception as e:
            logger.error(f"Not able to save test case result with error {e.args}")
            return ''
        
    def get_single_core_dump_via_job_id(self, job_id):
        single_core_dump = self.session.query(CoreDumpDetail).filter(CoreDumpDetail.njs_job_id == int(job_id))
        return single_core_dump[0]

    def save_core_dump_info(self, core_dump_summary):
        core_dump_summary_reorganized = []
        for suite_owner, core_dumps_info in core_dump_summary.items():
            for core_dump_info in core_dumps_info:
                core_dump_info.setdefault("Owner", suite_owner)
                core_dump_summary_reorganized.append(core_dump_info)

        for item in core_dump_summary_reorganized:
            if not self.session.query(CoreDumpDetail).filter_by(njs_job_id=int(item['NJS Job Id'])).first():
                coredump_record = CoreDumpDetail(
                    coredump_generated_time=item['Coredump Generated Time'],
                    coredump_url=item['Coredump URL'],
                    njs_job_id=int(item['NJS Job Id']),
                    product_name=item['Product Name'],
                    resource_id=int(item['Resource ID']),
                    software_version=item['Software Version'],
                    testsuite_display_name=item['Testsuite Display Name'],
                    owner=item['Owner']
                )
                self.session.add(coredump_record)
        self.session.commit()
        return core_dump_summary_reorganized       
        
    def get_aio_key_mapping(self):
        for i in range(0,5):
            print('111')
            all_records = self.session.query(AIO).all()
            key_map={}
            for record in all_records:
                key_map[record.aio_key]=record.aio_id
            if key_map:
                return key_map
            logger.info('Rollback in function get_aio_key_mapping.')
            self.session.rollback()
            time.sleep(2)

# if __name__ == '__main__':
#
#      sa = SonicAuto()
#      id = sa.get_product_id_from_platform('5600')
#      print(sa.get_session_group_name('6.2.7.1-21n', id))
#      sa.exit()
#
#     command = "python3 /tmp/unittest/eu_test_suite.py"
#     log_location = "/Results/logs"
#
#     sa.args['qbsjobid'] = '9016408'
#     sa.args['command'] = command
#     sa.args['log_location'] = log_location
#     sa.args['g_cc'] = 'snataraj'
#     sa.args['g_testbed'] = 'VTB522'
#     sa.args['g_avt_mountpoint'] = 'null'
#     sa.args['g_build'] = '/logs/downloads/snataraj-1550940730068_fake_fw.sig'
#     sa.args['g_product'] = '5600'
#     sa.args['g_scmlabel'] = 'cc_weekly_ui_rerun[23-02-2019]'
#     sa.args['g_user'] = 'snataraj'
#     sa.args['g_requesttime'] = '2019-02-23 08:59:58'
#     sa.args['g_qbs'] = '1'
#     sa.args['bundle'] = 'snataraj-1550940730068'
#     sa.args['path'] = '//depot/SQA/SWIFT4.0/TESTS/SonicOS/SST/GAV_Evasion/testsuites/gav_evasion.cts'
#     sa.args['starttime'] = '2019-02-24 09:00:00'
#
#     job_requestid = sa.save_job_request()
#
#     tc_result = {
#         'matrixid': '',
#         'job_requestid': job_requestid,
#         'type': 'TestCase',
#         'title': 'This is a test for PythonRunner',
#         'parameters': '--g_cc=test',
#         'alias': '',
#         'result': 'PASSED',
#         'starttime': '',
#         'endtime': '',
#         'filename': 'unittest.py',
#         'log_link': '/tmp/pythonrunner/logs.txt',
#         'uuid': '1234-2345-4567-7890'
#     }
#
#     sa.save_test_case_result(tc_result)
#
#     sa.exit()
