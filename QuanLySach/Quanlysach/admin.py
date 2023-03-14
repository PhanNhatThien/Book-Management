from Quanlysach import app, db, utils
from flask_admin import Admin , BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from Quanlysach.models import Category, Product, User, UserRole, Receipt, ReceiptDetail, Book_Entry
from flask_login import logout_user, current_user
from flask import redirect,request
from datetime import datetime



class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN

class ProductView(ModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    can_edit = False
    can_delete = False
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    column_exclude_list = ['image', 'created_date','active']
    column_labels = {
        'id': 'STT',
        'name': 'Tên sách',
        'description': 'Thể loại',
        'price': 'Giá',
        'image': 'Ảnh sách',
        'category': 'Danh mục'
    }
    column_sortable_list = ['id','name','price']

    def is_accessible(self):
        return (current_user.is_authenticated and current_user.user_role == UserRole.ADMIN) or (current_user.is_authenticated and current_user.user_role == UserRole.NGUOIQUANLYKHO)



class Book_EntryView(ModelView):
    column_display_pk = True
    can_view_details = True
    can_export = True
    can_edit = False
    can_delete = False
    column_searchable_list = ['name', 'description']
    column_filters = ['name', 'price']
    column_exclude_list = ['image', 'created_date','active']
    column_labels = {
        'id': 'STT',
        'name': 'Tên sách',
        'description': 'Thể loại',
        'price': 'Giá',
        'image': 'Ảnh sách',
        'category': 'Danh mục'
    }
    column_sortable_list = ['id','name','price']




class ReceiptDetailView(AuthenticatedModelView):
    column_display_pk = True
    column_labels = {
        'receipt.id': 'Hóa đơn',
        'product': 'Sách',
        'quantity':'Số lượng',
        'unit_price':'Đơn giá'
    }
    column_searchable_list = ['receipt.id']


class ReceiptView(AuthenticatedModelView):
    column_display_pk = True
    column_searchable_list = ['id','user.name']




class AuthenticatedBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class LogoutView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        logout_user()

        return redirect('/admin')



class BookEntryView(AuthenticatedBaseView):
    @expose('/')
    def index(self):

        return self.render('admin/book_entry.html')


class StatsView(AuthenticatedBaseView):
    @expose('/')
    def index(self):
        kw = request.args.get('kw')
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')
        year = request.args.get('year', datetime.now().year)

        return self.render('admin/stats.html',
                           month_stats=utils.product_month_stats(year=year),
                           stats=utils.product_stats(kw=kw,
                                                     from_date=from_date,
                                                     to_date=to_date))







class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html',
                           stats=utils.category_stats())

admin = Admin(app=app, name="Quản lý nhà sách", template_mode='bootstrap4', index_view=MyAdminIndex())
admin.add_view(AuthenticatedModelView(Category, db.session, name='Danh mục sách'))
admin.add_view(ReceiptDetailView(ReceiptDetail, db.session, name='CT - hóa đơn'))
admin.add_view(ReceiptView(Receipt, db.session, name='Hóa đơn'))
admin.add_view(ProductView(Product, db.session, name='Quản lý sách'))
admin.add_view(Book_EntryView(Book_Entry, db.session, name='Quản lý sách 2'))
admin.add_view(AuthenticatedModelView(User, db.session, name='Quản lý User'))
admin.add_view(StatsView(name='Thống kê báo cáo'))
admin.add_view(BookEntryView(name='Nhập sách'))
admin.add_view(LogoutView(name='Đăng xuất'))