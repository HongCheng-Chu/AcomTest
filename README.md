# AcomTest
Linux上讀取資料，Window上開發  
都是以python做開發，沒有用到javascript，我對javascript沒有很熟練

## 網頁  

### 主程式:   
分為五種路由
- home: 首頁，顯示DNS數據
- search: 顯示搜尋結果
- login: 登入
- logout: 登出
- register: 註冊

### 副程式:  
sqlbox.py 內有 class acomManager, acomManager 包含以下幾種 func :  
- _readCsv: 讀取 csv 檔案並轉換成 json  
- _create_db: 建立資料庫  
- import_db: 將csv匯入資料庫  
- get_dns: 從資料庫內取得資料  
- check_dns: 從資料庫內取得特定需求的資料  
- get: login 網頁內登入所需密碼的取得  
- push: register 網頁內將資料放進資料庫中  
- check: 檢查燈速帳密是否正確  

## Q1. csv檔案放入資料庫
 -在 import_db func 內  
- import_db 流程:  
  _create_db -> readCsv -> MySQL

## Q2. 網頁實作

1. 首頁: home.html  
- 流程: route home -> import_db -> get_db -> output  
2. 登入頁: login.html  
- 流程: route home -> click login -> 輸入帳密或註冊資料 -> 跳回 home
3. 註冊頁: register.html  
- 流程: route home -> click register -> 註冊資料 -> 跳回 logiin  
4. 搜尋結果頁: search.html  
-流程: route home -> 輸入資料(4種都需輸入) -> 開新分頁顯示資料  

