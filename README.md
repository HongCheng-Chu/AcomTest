# AcomTest
Linux上讀取資料，Window上開發

## Q1. 讀取dsn_sample.csv資料併存進MySQL  
sqlbox.py 內有 class acomManager, acomManager 包含以下幾種 func :  
- _readCsv: 讀取 csv 檔案並轉換成 json  
- _create_db: 建立資料庫  
- import_db: 將csv匯入資料庫  
- get_dns: 從資料庫內取得資料  
- check_dns: 從資料庫內取得特定需求的資料  
- get: login 網頁內登入所需密碼的取得  
- push: register 網頁內將資料放進資料庫中  
- check: 檢查燈速帳密是否正確  
