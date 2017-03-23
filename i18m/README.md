
### PROCESS FLOW

1. 登录

	1.1
	1.2 https://www-304.ibm.com/usrsrvc/account/userservices/jsp/login.jsp?persistPage=true&page=/financing/gars/ptx/command/CookieErrorView%3FstoreId%3D10001%26langId%3D-1&PD-REFERER=http://www-03.ibm.com/financing/us/gars/imcptx/index.html&error=

2. 登录成功后进入欢迎页

	https://www-304.ibm.com/financing/gars/ptx/command/WelcomeView

3. 进入分类列表页面，点击pc notebooks

	https://www-304.ibm.com/financing/gars/ptx/command/TopCategoriesDisplay?storeId=13834&catalogId=10001&langId=-1&geoId=16463

4. 显示pc notebooks产品列表，勾选产品加购物车

	https://www-304.ibm.com/financing/gars/ptx/command/CategoryDisplay?catalogId=10001&storeId=13834&langId=-1&categoryId=16540&parent_category_rn=16463&isProd=true&usePagination=true&geoId=16463

5. 显示购物车详情， checkout
        
    https://www-304.ibm.com/financing/gars/ptx/command/ShoppingCartDisplay?krypto=u2qyvGmHPwnF%2BYjOHU5XvJxIhM9mtfPYuhWoe%2FxOox0abHcTDdLma03NBcDjFDnYJXbpXrVRGMmWfkAyO%2Ft7EG5YqJH9XRCUdul2fqeCbniD6Y6MsXB66xkZDaukHWugV%2Fy7ZjhKrofAo77uirlg9A%3D%3D&ddkey=https%3ARetainUserSelectionCmd


6. checkout 1/2 填写信息
    https://www-304.ibm.com/financing/gars/ptx/command/OrderCheckoutView?krypto=tElV%2BNsaH7d2BUJ4M5YoSAWnVQjc%2FvsIKFgxopJAf5okq1u7YDQjifzXh2LhcA%2BP5DTTCg4h6IR%2BuadbcPko36MzaL0Cinv4qWq%2BqjCfM45V31UBxSfpnKYhucSwwwdA&ddkey=https%3AURLRedirectCmd

7. checkout 2/2 确认信息并submit


#### example

	from selenium.webdriver.common.by import By
	from selenium.webdriver.support.ui import WebDriverWait
	from selenium.webdriver.support import expected_conditions as EC

	element = WebDriverWait(driver, 10).until(
	    EC.element_to_be_clickable((By.ID, "myDynamicElement"))
	)
	element.click()
