from flask import json, request,jsonify,render_template,flash,redirect, url_for, send_file
import pandas as pd
from app import db, app
from model.Employee import Employee

class EmployeeController:
    
    def index(self):
        return render_template("index.html")

    def employee(self):
        return render_template("emp_form.html")
    
    def add_employee(self):
        
        f = request.files['file']
        f.save(r"uploads/" + f.filename)
        new_employee = Employee(username=request.form.get("username"), email=request.form.get("email"),\
                               address=request.form.get("address"), file_name=f.filename)
        try:
            db.session.add(new_employee)
            db.session.commit()
            return redirect(url_for('paging_emp'))
        except Exception as e:
            return jsonify({"status": "fail"})
    
    def paging(self):
        page = int(request.args.get("page")) if request.args.get("page") is not None else 1
        results_per_page = int(request.args.get("results_per_page")) if request.args.get("results_per_page") is not None else 10
        if page == 0:
            page == 1
            
        filter_name = ''
        if request.args.get('search') is not None:
            filter_name = request.args.get('search')
        
        records = db.session.query(Employee).filter(Employee.username.like('%' + filter_name + '%'))
        count = records.count()
        records = records.limit(results_per_page).offset((page-1)*results_per_page).all()
        if records is not None:
            obj_result = {
                "total": count,
                "page": page,
                "results_per_page": results_per_page,
                "data": self.process_data(records)
            }
            return render_template('index.html', result = obj_result)
        else:
            return jsonify([])

    def process_data(self, records):
        list_result = []
        for item in records:
            if item.file_name == None:
                item.file_name = "Not found"
            list_result.append(item.obj_person())
        
        return list_result

    def edit_employee(self, emp_id):
        record_exist = db.session.query(Employee).filter(Employee.id == emp_id).first()
        if record_exist is not None:
            try:
                f = request.files['file']
                f.save(r"uploads"+f.filename)
            except:
                f.filename = record_exist.file_name
            record_exist.username = request.form.get("username")
            record_exist.email = request.form.get("email")
            record_exist.address = request.form.get("address")
            record_exist.file_name = f.filename
            db.session.add(record_exist)
            db.session.flush()
            db.session.commit()
            return redirect(url_for('paging_emp'))

    def get_by_id(self, id):
        record_exist = db.session.query(Employee).filter(Employee.id == id).first()
        if record_exist is not None:
            return jsonify(record_exist.obj_person())
        else:
            return jsonify({"err": "not found"})
    
    def get_emp_by_id(self):
        emp_id = request.args.get("id")
        record_exist = db.session.query(Employee).filter(Employee.id == int(emp_id)).first()
        if record_exist is not None:
            if record_exist.file_name is None:
                record_exist.file_name = "Not found"
            return render_template("emp_form_edit.html", data=record_exist.obj_person())

    def delete_employee(self, emp_id):
        record_exist = db.session.query(Employee).filter(Employee.id == emp_id).first()
        if record_exist is not None:
            db.session.delete(record_exist)
            db.session.commit()
            return redirect(url_for('paging_emp'))

    def import_excel(self):
        try:
            f = request.files['file']
            if f is not None:
                df = pd.DataFrame(pd.read_excel(f))
                len_data = len(df)
                for i in range(0, len_data):
                    row = df.loc[i]
                    new_emp = Employee(row[0], row[1], row[2], "None")
                    db.session.add(new_emp)
                    db.session.commit()
        
                return redirect(url_for('paging_emp'))
        except Exception as e:
            print("error")
            return redirect(url_for('paging_emp'))
    def download_file(self):
        file_name = request.args.get("file_name") if request.args.get("file_name") is not None else ""
        #check file existed
        return send_file(r"uploads/"+ file_name, as_attachment=True)

employ_controller = EmployeeController()

app.add_endpoint("/", "index", employ_controller.paging)
app.add_endpoint("/employees", "employees", employ_controller.employee)
app.add_endpoint("/add_employee", "add_employee", employ_controller.add_employee, methods=['POST'])
app.add_endpoint("/details", "details", employ_controller.get_emp_by_id)
app.add_endpoint("/edit_employee/<int:emp_id>", "edit_employee", employ_controller.edit_employee, methods=['POST'])
app.add_endpoint("/delete_employee/<int:emp_id>", "delete_employee", employ_controller.delete_employee)
app.add_endpoint("/employee/<int:id>", "employee", employ_controller.get_by_id, methods=['GET'])
# app.add_endpoint("/list_emloyee", "list_employee", employ_controller.show_list_employee, methods=['GET'])
app.add_endpoint("/list_emloyee/paging_emp", "paging_emp", employ_controller.paging, methods=['GET'])
app.add_endpoint("/download", "download", employ_controller.download_file, methods=['GET', 'POST'])
app.add_endpoint("/import_excel", "import_excel", employ_controller.import_excel, methods=['POST'])