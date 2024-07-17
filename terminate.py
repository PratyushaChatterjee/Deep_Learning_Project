import os

def terminate_program(program_path):
    try:
        os.system(f'taskkill /F /IM python.exe /FI "LocationEquality {program_path}"')
    except Exception as e:
        print(f'Error: {e}')

# Example usage
program_path=r"D:\SMART_BENGAL\pest.py"
