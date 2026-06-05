# This file is to create and update csv results

import os
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, Border, Side

from pytest_resources.common_require import *
from inputs.constants import *
from libs.fw_configuration import FWConfiguration
from libs.mail import MailModule


class CSVGenerator:

    # Create new CSV file to update Testcase Results
    def generate_csv_file(self, login_method, file_name):
        login_method_dir_path = os.path.join(csv_dir_path, login_method)
        os.path.exists(login_method_dir_path) or os.makedirs(login_method_dir_path)
        csv_file_name = os.path.join(login_method_dir_path, str(file_name) + ".csv")
        logger.info("opening " + csv_file_name + " file for writing test case results")
        output_file = open(csv_file_name, 'w', newline='')
        output_writer = csv.writer(output_file)
        output_writer.writerow(['Login Method', 'Login Group', 'Authentication Method', 'Authentication Factor', "User",
                                'Credential Type', 'RESULT'])
        output_file.close()
        return True

    # Update Testcase Results in CSV file
    def update_results_to_csv(self, file_name, login, group, auth, factor, user, cred_type, result):
        csv_file_name = os.path.join(csv_dir_path, login, str(file_name) + ".csv")
        output_file = open(csv_file_name, 'a', newline='')
        a = csv.writer(output_file, delimiter=',')
        a.writerow([login, group, auth, factor, user, cred_type, result])
        output_file.close()
        return True

    # Check Response and update final result
    def response_checker(self, response):
        if response is True:
            result = "PASSED"
        else:
            result = "FAILED"
        return result

    # Combine all individual csv files into one csv file
    def combine_all_csv_files(self):
        # Specify the file to exclude
        exclude_file = 'sonicos_authentication_test.csv'
        # Initialize an empty list to hold dataframes
        dataframes = []
        # Walk through the directory and its subdirectories
        for dirpath, _, filenames in os.walk(csv_dir_path):
            for filename in filenames:
                if filename.endswith('.csv') and filename != exclude_file:
                    filepath = os.path.join(dirpath, filename)
                    df = pd.read_csv(filepath)
                    dataframes.append(df)
        # Concatenate all dataframes
        consolidated_df = pd.concat(dataframes, ignore_index=True)

        # Calculate the number of Passed and Failed entries
        pass_count = consolidated_df['RESULT'].str.lower().value_counts().get('passed', 0)
        fail_count = consolidated_df['RESULT'].str.lower().value_counts().get('failed', 0)
        # Calculate the pass percentage
        total_count = pass_count + fail_count
        pass_percentage = (pass_count / total_count * 100) if total_count > 0 else 0

        # Create an Excel writer object
        file_name = 'SonicOS_Auth_Hardening_Test'
        output_file = os.path.join(results_dir_path, "csv", str(file_name) + ".xlsx")
        with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
            consolidated_df.to_excel(writer, index=False, sheet_name='Sheet1')
            workbook = writer.book
            worksheet = writer.sheets['Sheet1']
            # Define fonts for Passed (Green) and Failed (Red)
            green_font = Font(color='00FF00', bold=True)
            red_font = Font(color='FF0000', bold=True)
            # Apply formatting to the Result column
            for row in range(2, len(consolidated_df) + 2):  # +2 because Excel is 1-indexed and includes header
                cell = worksheet.cell(row=row, column=consolidated_df.columns.get_loc('RESULT') + 1)
                if cell.value.lower() == 'passed':
                    cell.font = green_font
                elif cell.value.lower() == 'failed':
                    cell.font = red_font
            # Customize header row style (left-align and remove borders)
            header_row = worksheet[1]
            for cell in header_row:
                cell.alignment = Alignment(horizontal='left')
                cell.border = Border(top=None, left=None, right=None, bottom=None)

        # Consolidating the result into a list
        results = [pass_count, fail_count, total_count, pass_percentage]
        logger.info(results)
        return results

    # Mail the combined CSV file with results
    def send_combined_results_csv(self, results):

        # Get FireWall details to include in the email
        fw_obj = FWConfiguration()
        response = fw_obj.get_fw_details()
        fw_version = response['firmware_version']
        fw_model = response['model']

        # Output file path
        file_name = "SonicOS_Auth_Hardening_Test.xlsx"
        combined_results_csv_file = os.path.join(results_dir_path, "csv", str(file_name))
        attachment_path = combined_results_csv_file

        # Create the detailed email body
        # html mail body style tags
        html_style = ('''<style>table {
                  font-family: Verdana;
                  border:1px solid black;
                  font-size: 14px;
                  width:50%;
                }
                caption {
                  text-align: center;
                  color: #FF0000;
                  padding: 5px;
                }
                td{
                  word-break: break-all;
                  padding: 5px 10px;
                  border:1px solid black;
                  }
                th{
                  padding: 5px 10px;
                  text-align: left;
                  font-weight: normal;
                  background: #0096FF;
                  color: #FFF;
                  border:1px solid black;
                }</style>''')

        html_body = ('<table><caption>SonicOS Authentication Hardening Test Results</caption>'
                     '    <tr>'
                     '      <th>FireWall Type</th>'
                     '      <td>{fw_model}</td>'
                     '    </tr>'
                     '    <tr>'
                     '      <th>Firmware Version</th>'
                     '      <td>{fw_version}</td>'
                     '    </tr>'
                     '    <tr> %s'
                     '    </tr>'
                     '</table>').format(fw_model=fw_model, fw_version=fw_version)

        results_info = """
        <th>Total executed testcases:</th><td>{total_count}</td></tr>
        <tr><th>Passed testcases:</th><td><font color='green'>{pass_count}</td></tr>
        <tr><th>Failed testcases:</th><td><font color='red'>{fail_count}</td></tr>
        <tr><th>Pass percentage:</th><td>{pass_percentage:.2f}%</td></tr>
        """.format(pass_count=results[0], fail_count=results[1], total_count=results[2], pass_percentage=results[3])

        message_start = """<html>
        <body>
        <p>Hello,</p>
        <p>Please find the attached combined CSV results file.</p>
        <p>Summary of the results:</p>
        </body>
        </html>
        """

        message_end = """<html>
        <body>
        <p>Best Regards,<br>Team Automation</p>
        </body>
        </html>
        """

        mail_body = html_style + message_start + html_body % results_info + message_end

        # Email details
        sender_email = sender_email_id
        recipient_emails = recipient_email_list
        subject = 'SonicOS Auth Hardening Test Run completed for - ' + fw_version +\
                  '. Result : PASSED: ' + str(results[0]) + ', FAILED: ' + str(results[1])
        smtp_port_number = 25

        mail_obj = MailModule()
        mail_obj.send_email_with_attachment(sender_email, recipient_emails, subject, mail_body, attachment_path,
                                            file_name, sv_web_mail_server, smtp_port_number)

