import psutil

def close_chrome():
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if 'chrome' in proc.info['name'].lower():
            print(f"Terminating Chrome process with PID: {proc.info['pid']}")
            proc.terminate()


close_chrome()
