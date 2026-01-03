# Bookswap-and-StudyGroup-
A system for manage borrowing book process and group studying

## Requirement  
fastapi[all]  
sqlmodel psycopg[binary]  
python-jose[cryptography]  
bcrypt==3.2.0  

## Các cải tiến  
Tăng cường bảo mật  
Tối ưu, code gọn hơn  

## Chức năng cơ bản:
+ Tạo và tìm kiếm người dùng
+ Tạo, tìm kiếm, cập nhật và xóa sách
+ Tạo, tìm kiếm các yêu cầu muốn trao đổi sách (Từ chối/ chấp nhận yêu cầu giao dịch sẽ gửi thông báo cho id requester).
+ Tạo, tìm kiếm, tham gia vào các nhóm học tập.

## Cấu trúc project 
app
+ main (Nhánh chính)
+ models (BaseModel)
+ deps (Depends, các hàm trợ giúp)
+ db (database)
+ respositories (các thao tác liên quan đến PostgreSQL)
+ routers (Các nhánh phụ)
  + users
  + books
  + listings (listing + swap_request)
  + study groups
  + notifications
db (tạo bảng và insert sample data trên PostgreSQL)

 ## Run project 
 fastapi dev app/main.py 
