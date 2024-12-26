import uiautomator2

d = uiautomator2.connect()

d.app_start("com.hexin.plat.android")
jine = d(resourceId="com.hexin.plat.android:id/capital_cell_value")[3]
print(jine.get_text())