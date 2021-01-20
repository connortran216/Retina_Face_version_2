import logging
import os

savepath = "path/to/save/at/"

# if not os.path.exists(savepath):
logging.critical("‘Warning! The savepath provided doesn\’t exist!'Saving at current directory ‘")
# savepath = os.getcwd()
# logging.info("‘savepath reset at %s’", str(savepath))
# # else:
# 	logging.info("'Savepath provided is correct, saving at %s’", str(savepath))