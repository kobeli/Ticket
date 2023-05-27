class User:
    def __init__(self, e_id, book_date, patient_id, phoneNumber, password, idCard, patient_name):
        # 专家id
        self.e_id = e_id
        # 日期
        self.book_date = book_date
        # 病人id
        self.patient_id = patient_id
        # 病人账号
        self.phoneNumber = phoneNumber
        # 病人密码
        self.password = password
        # 身份证
        self.idCard = idCard
        # 姓名
        self.patient_name = patient_name
