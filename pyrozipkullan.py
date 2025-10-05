import pyroSAR
file = "S1A_IW_GRDH_1SDV_20210723T155034_20210723T155059_038907_049743_FA4D.zip"
sd = pyroSAR.identify(file)
print(sd)
print("#################")
print(sd.export2dict())