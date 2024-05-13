import subprocess

activate_env = r'C:\Users\charl\Desktop\AutoOffer\Scripts\activate.bat'
subprocess.call(activate_env, shell=True)

process1 = subprocess.Popen(["python", "AutoOffer\html_manipulation\Property_Data_Sender.py"]) # Create and launch process pop.py using python interpreter
process2 = subprocess.Popen(["python", "AutoOffer\html_manipulation\html_manipulation\Asyc_GHL_Checker.py"])
process3 = subprocess.Popen(["python", "AutoOffer\Offer_Generator\Offer_Maker.py"])

process1.wait() # Wait for process1 to finish (basically wait for script to finish)
process2.wait()
process3.wait()