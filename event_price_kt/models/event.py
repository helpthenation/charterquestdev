
from io import StringIO
from odoo import fields, models, api, _
from odoo.tools.translate import _
from datetime import datetime, timedelta
from odoo.exceptions import Warning, ValidationError
import base64
from odoo import netsvc

class class_attendance(models.Model):
    _name = "event.class.attendance"

    student_ids = fields.Many2many("res.partner",'event_class_students_attendance','class_id','sudent_id',"Students")
    class_name = fields.Char("Class Name",size=256)
    date = fields.Datetime("Date and time")
    event_id = fields.Many2one("event.event","Event")
    status = fields.Selection([('present','Present'),('absent','Absent')],"Attendance")
    comment = fields.Text("Comments")


class event_subject(models.Model):
    _name = "event.subject"

    name = fields.Char('Name')


class event_event(models.Model):

    _inherit = 'event.event'
#    _order = "date_begin asc"

    pc_exam = fields.Boolean('PC Exam', help="Tic this to view PC Exam types")
    type_pc_exam = fields.Many2one('pc.exam.type', "Type of PC Exam")
    # seats_available = fields.Integer('Seats Availability')
    month = fields.Integer('Month')
    day = fields.Integer('day')
    product_ids = fields.Many2many('product.product', 'event_product_rel','event_id', 'product_id', "Products")
    class_attendance_ids = fields.One2many("event.class.attendance", 'event_id', "Class Attendance")
    subject = fields.Many2one("event.subject", "Subject")

    # @api.model
    # def search(self, cr, user, args, offset=0, limit=None, order=None, context=None, count=False):
    #     return super(event_event, self).search(cr, user, args, offset=offset, limit=limit, order=order, context=context, count=count)

    # @api.model
    # def create(self, cr, uid, vals, context=None):
    #     """ To write the Number of seats available """
    #     if 'date_begin' in vals.keys() and not vals.get('month',False):
    #         date_begin = datetime.strptime(vals['date_begin'], "%Y-%m-%d %H:%M:%S")
    #         vals['month'] = date_begin.month
    #         vals['day'] = date_begin.day
    #     if 'seats_max' in vals.keys():
    #          vals['seats_available'] = vals['seats_max']
    #     return super(event_event, self).create(cr, uid, vals, context)

    # @api.multi
    # def onchange_start_date(self, cr, uid, ids, date_begin=False, date_end=False, context=None):
    #     res = {'value': {}}
    #     if date_end:
    #         return res
    #     if date_begin and isinstance(date_begin, str):
    #         date_begin = datetime.strptime(date_begin, "%Y-%m-%d %H:%M:%S")
    #         date_end = date_begin + timedelta(hours=1)
    #         month = str(date_begin).split('-')[1]
    #         day = str(date_begin).split('-')[2].split(' ')[0]
    #         res['value'] = {'date_end': date_end.strftime("%Y-%m-%d %H:%M:%S"),'month':int(month),'day':int(day)}
    #
    #     return res

    # @api.multi
    # def get_data_event(self, cr, uid, id, context=None):
    #     val =  self.read(cr, uid, id,[],context)
    #     context={'lang': 'en_US', 'calendar_default_user_id': 1, 'tz': 'Africa/Johannesburg', 'uid': 1}
    #     for i in val:
    #         obj= self.browse(cr,uid,i['id'],context)
    #         i['date_begin']=obj.date_begin
    #         i['date_end']=obj.date_end
    #     return val

#     @api.multi
#     def get_attendance_report(self,cr,uid,ids,context=None):
#
#         try:
#             import xlwt
#         except:
#             raise Warning(_('User Error'), _('Please Install xlwt Library.!'))
#         filename = 'Attendance Register.xls'
#         fp = cStringIO.StringIO()
#         wb = xlwt.Workbook(encoding='utf-8')
#
#         worksheet = wb.add_sheet('PC_EXAM_ATTENDANCE_REGISTER')
#         current_obj=self.browse(cr,uid,ids)[0]
#
# #        -----------------------
# #        Excel Font Style & Sizes
# #        ----------------------
#         fnt1 = Font()
#         fnt1.name = 'TimesNewRoman'
#         fnt1.bold = True
#         fnt1.height = 16*0x14
#
#         fnt2 = Font()
#         fnt2.name = 'verdana'
#         fnt2.bold = True
#         fnt2.height = 12*0x14
#
#
#         fnt3 = Font()
#         fnt3.name = 'TimesNewRoman'
#         fnt3.bold = True
#         fnt3.height = 13*0x12
#
#         fnt4 = Font()
#         fnt4.name = 'TimesNewRoman'
#         fnt4.height = 16*0x14
#
# #    -----------------
# #    Excel  Alignment
# #    ----------------
#         al3 = Alignment()
#         al3.horz = Alignment.HORZ_CENTER
#         al3.vert = Alignment.VERT_CENTER
#
#         al4 = Alignment()
#         al4.horz = Alignment.HORZ_LEFT
#         al4.vert = Alignment.VERT_CENTER
#
#         al5 = Alignment()
#         al5.horz = Alignment.HORZ_LEFT
#         al5.vert = Alignment.VERT_CENTER
# #    -----------------------
# #    Excel  Style
# #    ----------------------
#
#         style1 = XFStyle()
#         style1.alignment = al3
#         style1.font=fnt1
#
#         style2 = XFStyle()
#         style2.font=fnt2
#         style2.alignment=al4
#
#
#
#         style3 = XFStyle()
#         style3.alignment = al3
#         style3.font=fnt3
#
#         style4 = XFStyle()
#         style4.alignment = al5
#         style4.font=fnt4
# #-------------------------------------------------------------------------
# #                         HEADER In Excel
# #-------------------------------------------------------------------------
#
#         lst=[]
#
#         fields=['CIMA STUDENT NUMBER','SURNAME','NAME','SIGNATURE']
#         for i in [1,2,3,4]:
#             first_col = worksheet.col(i)
#             first_col.width = 500 * 20
#
#         date_begin = str(datetime.strptime(current_obj.date_begin, "%Y-%m-%d %H:%M:%S")+timedelta(hours=2))
#         date_end = str(datetime.strptime(current_obj.date_end, "%Y-%m-%d %H:%M:%S")+timedelta(hours=2))
#
#         worksheet.merge(0, 16, 1, 4)
#         try:
#            worksheet.insert_bitmap('/opt/custom_modules/event_price_kt/images/charterquest.bmp',0, 1, 9, 3)
#         except:
#              pass
#         worksheet.write_merge(17,18,1 ,1 ,'SUBJECT:', style1)
#         worksheet.write_merge(17,18,2, 4,current_obj.name , style1)
#         k = 19
#         pc_exam = True
#         if current_obj.pc_exam == False:
#            pc_exam = False
#            worksheet.write_merge(k,k+1,1 ,1 ,'LECTURER:', style1)
#            #if current_obj.main_speaker_id:
#            #    worksheet.write_merge(k,k+1,2, 4,current_obj.main_speaker_id.name , style1)
#            #else:
#            #    worksheet.write_merge(k,k+1,2, 4,"", style1)
#            k = k+2
#         worksheet.write_merge(k,k+1,1 ,1 ,'DATE:', style1)
#         worksheet.write_merge(k,k+1,2, 4,(date_begin).split(' ')[0] , style1)
#         worksheet.write_merge(k+2,k+3,1 ,1 ,'TIME:', style1)
#         worksheet.write_merge(k+2,k+3,2, 4,(date_begin)[11:16]+'-'+(date_end)[11:16], style1)
#         if not pc_exam:
#             worksheet.write_merge(k+4,k+5,1 ,1 ,'COURSE STUDY OPTION:', style1)
#             worksheet.write_merge(k+4,k+5,2, 4,current_obj.study.name, style1)
#             k = k+4
#         else:
#             k = k+2
#         worksheet.write_merge(k+2,k+3,1 ,1 ,'CAMPUS:', style1)
#         worksheet.write_merge(k+2,k+3,2, 4,current_obj.address_id.name, style1)
#         worksheet.write_merge(k+4,k+5,1, 4,"PLEASE SIGN ATTENDANCE REGISTER & ENTER CIMA STUDENT NUMBER", style1)
#         i=1
#         for field in fields:
#             worksheet.write_merge(k+6,k+7,i ,i ,field, style1)
#             i+=1
#         i=k+8
#
#
#         for obj in current_obj.registration_ids:
#             partner_name = obj.partner_id.name
#             name = partner_name.split('  ')
#             if len(name)==1:
#                 name = partner_name.split(' ')
#             if obj.partner_id.prof_body_id:
#                 worksheet.write_merge(i,i+1,1,1,obj.partner_id.prof_body_id,style4)
#             else:
#                 worksheet.write_merge(i,i+1,1,1,"",style4)
#             try:
#                 worksheet.write_merge(i,i+1,2,2,name[1],style4)
#             except:
#                    worksheet.write_merge(i,i+1,2,2,'',style4)
#             worksheet.write_merge(i,i+1,3,3, name[0],style4)
#             worksheet.write_merge(i,i+1,4,4,'',style4)
#             i+=2
#
#         wb.save(fp)
#         out = base64.encodestring(fp.getvalue())
#         final_arr_data = {}
#         final_arr_data['file_stream'] = out
#         final_arr_data['name'] = filename
#         pl_report_id=self.pool.get('attendance.sheet.report').create(cr, uid, final_arr_data, context={})
#         vals={
#               'name':'Attendance Sheet Report',
#               'datas':out,
#               'datas_fname':filename
#               }
#
#       #  return {'file_stream':out, 'file_name': filename}
#         return {
#             'res_id'   : pl_report_id,
#             'name'     : filename,
#             'view_mode': 'form',
#             'res_model': 'attendance.sheet.report',
#             'type'     :'ir.actions.act_window',
#             }


class attendance_sheet_report(models.AbstractModel):
    _name = "attendance.sheet.report"
    _description = "To generate attendance Sheet"

    file_stream = fields.Binary('File Stream')
    name = fields.Char('File Name', size=255)


class event_type(models.Model):
    _inherit = "event.type"

    discount = fields.Float('Discount (%)')
    professional_body_code = fields.Char('Professional Body Code',size=64)
    order = fields.Integer('Order')


class event_registration(models.Model):
    _inherit = 'event.registration'

    # @api.multi
    # def _get_event(self, cr, uid, ids, name, arg, context=None):
    #      res = {}
    #      for obj in self.browse(cr, uid, ids, name, arg, context=context):
    #          res[obj.id] = False
    #          if obj.event_id.pc_exam:
    #               res[obj.id] = True
    #      return res

    # pc_exam = fields.Boolean(compute='_get_event' ,string="PC Exam")
    pc_exam = fields.Boolean(string="PC Exam")
    reg_prof_body = fields.Selection([('yes','YES'),('no','NO')], string='Registered with Professional Body',help="Student is Registered with Professional Body?")
    pc_exam_marks = fields.Integer(string='PC Exam Marks')
    pc_exam_result = fields.Selection([('passed','Passed'),('failed','Failed')],string='PC Exam Result')
    start_d = fields.Datetime(string="start date")
    end_d = fields.Datetime("end date")
    encoded_reg_link = fields.Char("Encoded Registration Link")

    ######################Reschedule PC Exam Process

    # @api.multi
    # def event_reg_url(self, cr, uid, ids):
    #     """ Reschedule Url"""
    #     #server_url =  self.pool.get('ir.config_parameter').get_param('web.base.url')
    #     server_url = "http://pcexams.openerponline.co.za"
    #     import hashlib
    #     event_reg_id = ids[0]
    #     encoded_link = hashlib.sha224(str(event_reg_id)).hexdigest()
    #     self.write(cr, uid, event_reg_id, {'encoded_reg_link':encoded_link})
    #     url_pattern = server_url +'/reschedule/'+ encoded_link
    #     return url_pattern
    #
    # @api.multi
    # def registration_open(self, cr, uid, ids, context=None):
    #     if not len(ids) > 1:
    #         if self.browse(cr,uid,ids).need_rescheduling and not self.browse(cr,uid,ids).rescheduling_done:
    #                     template = self.browse(cr,uid,ids).event_id.email_registration_id
    #                     subject = 'Reschedule CharterQuest PC Exams Confirmation'+'  '+self.browse(cr,uid,ids).event_id.name
    #                     template.write({'subject':subject})
    #                     if template:
    #                             mail_message = template.send_mail(ids[0])
    #                     self.write(cr,uid,ids,{'need_rescheduling':False,'rescheduling_done':True})
    #
    #         if context==None:
    #                context = {}
    #         event_obj = self.pool.get('event.event')
    #         for register in  self.browse(cr, uid, ids, context=context):
    #             event_id = register.event_id.id
    #             no_of_registration = register.nb_register
    #             #event_obj.check_registration_limits_before(cr, uid, [event_id], no_of_registration, context=context)
    #             seats_available = register.event_id.seats_available-1
    #             registrations = len(self.pool.get('event.registration').search(cr,uid,[('event_id','=',event_id),('state','=','open')]))
    #             seats_available = register.event_id.seats_max-registrations-1
    #             self.pool.get('event.event').write(cr,uid,[event_id],{'seats_available':seats_available})
    #             #iTo change date time zone to SA
    #             dic={}
    #             dic['start_d']=str(datetime.strptime(register.event_id.date_begin, "%Y-%m-%d %H:%M:%S")+timedelta(hours=2))
    #             dic['end_d']=str(datetime.strptime(register.event_id.date_end, "%Y-%m-%d %H:%M:%S")+timedelta(hours=2))
    #             self.write(cr,uid,ids,dic)
    #
    #     if not len(ids) > 1:
    #             if self.browse(cr,uid,ids).need_rescheduling == False and self.browse(cr,uid,ids).need_rescheduling == False:
    #                 res = self.confirm_registration(cr, uid, ids, context=context)
    #                 self.mail_user(cr, uid, ids, context=context)


class pc_exam_type(models.Model):
   _name = 'pc.exam.type'

   name = fields.Char('Name',size=64,required=True)
   discount_amount = fields.Float("Discount Amount")
   type_event_id = fields.Many2one('event.type','Professional Body')


class sale_order(models.Model):
   _inherit = 'sale.order'
   _order = 'id desc'

   # @api.multi
   # def _get_no_of_days(self,cr,uid,ids,name,args,context=None):
   #    """To get number of days from the quotaion created date"""
   #
   #    res = {}
   #    for obj in self.browse(cr,uid,ids):
   #             res[obj.id] = ''
   #             today = datetime.now()
   #             order_date = datetime.strptime(obj.date_order,"%Y-%m-%d %H:%M:%S")
   #             days = today - order_date
   #             res[obj.id] = (str(days).split(','))[0]
   #    return res

   current_quote = fields.Boolean("Current Quote")
   pc_exam_type = fields.Many2one('pc.exam.type',"PC exam type")
   pc_exam = fields.Boolean('PC Exam')
   provisional_booking = fields.Boolean("Provisional Booking")
   link_portal = fields.Char("Link")
   #Fot payment page capture
   diposit_selected = fields.Integer("Selected Deposit %")
   due_amount = fields.Float('Total Due')
   months = fields.Integer("Months required to pay")
   out_standing_balance_incl_vat = fields.Float("Outstanding Balance (inclusive of VAT & Interest)")
   monthly_amount = fields.Float("Monthly Amount")
   # no_of_days = fields.Char(compute='_get_no_of_days', type='char',string='Days From requested date')

   no_of_days = fields.Char(type='char', string='Days From requested date')

   no_of_reminder_emails_sent = fields.Integer("No.of Reminder Emails Sent", default=0)
   freequote_opt_out = fields.Boolean("FreeQuote Opt-out")

   # _defaults = {
   #                 'no_of_reminder_emails_sent':0,
   #  }

   # @api.multi
   # def print_quotation(self, cr, uid, ids, context=None):
   #      '''
   #      This function prints the sales order and mark it as sent, so that we can see more easily the next step of the workflow
   #      '''
   #      assert len(ids) == 1, 'This option should only be used for a single id at a time'
   #      wf_service = netsvc.LocalService("workflow")
   #      wf_service.trg_validate(uid, 'sale.order', ids[0], 'quotation_sent', cr)
   #      datas = {
   #               'model': 'sale.order',
   #               'ids': ids,
   #               'form': self.read(cr, uid, ids[0], context=context),
   #      }
   #      return {'type': 'ir.actions.report.xml', 'report_name': 'sales_proforma_enrollment', 'datas': datas, 'nodestroy': True}

   # @api.multi
   # def send_freequote_remainder_email(self, cr, uid, context=None):
   #         """Email to send remainder about free quote"""
   #
   #         sale_order =  self.pool.get('sale.order')
   #         year = datetime.now().year
   #
   #         start_date = str(year)+"-01-01"
   #         end_date = str(year)+"-12-31"
   #
   #         draft_domain1 = [('state','=','draft'),('date_order','>=',start_date),('date_order','<=',end_date)]
   #         draft_domain = [('state','=','draft'),('date_order','>=',start_date),('date_order','<=',end_date)]
   #         order_domain = [('state','!=','draft'),('date_order','>=',start_date),('date_order','<=',end_date)]
   #
   #         sem1_ids = sale_order.search(cr,uid,draft_domain1+[('semester','=','1')])
   #         sem2_ids = sale_order.search(cr,uid,draft_domain1+[('semester','=','2')])
   #         sem1_filtered_ids = []
   #         sem1_objs = sale_order.browse(cr,uid,sem1_ids)
   #         for sale in sem1_objs:
   #                 partner = sale.partner_id.id
   #                 if sale_order.search(cr,uid,order_domain+[('semester','=','1'),('partner_id','=',partner)]):
   #                          continue
   #                 else:
   #                    try:
   #                        max_id = max(sale_order.search(cr,uid,draft_domain+[('semester','=','1'),('partner_id','=',partner)]))
   #                        sem1_filtered_ids.append(max_id)
   #                    except:
   #                         pass
   #
   #         sem2_filtered_ids = []
   #         sem2_objs = sale_order.browse(cr,uid,sem2_ids)
   #
   #         for sale in sem2_objs:
   #                 partner = sale.partner_id.id
   #                 if sale_order.search(cr,uid,order_domain+[('semester','=','2'),('partner_id','=',partner)]):
   #                          continue
   #                 else:
   #                    try:
   #                       max_id = max(sale_order.search(cr,uid,draft_domain+[('semester','=','2'),('partner_id','=',partner)]))
   #                       sem2_filtered_ids.append(max_id)
   #                    except:
   #                          pass
   #
   #         ids = list(set(sem1_filtered_ids + sem2_filtered_ids))
   #
   #         ##Updating current quote field
   #         current_quotes = sale_order.search(cr,uid,[('current_quote','=',True)])
   #         sale_order.write(cr,uid,current_quotes,{'current_quote':False})
   #         sale_order.write(cr,uid,ids,{'current_quote':True})
   #         ##End
   #         for sale_obj in self.browse(cr, uid, ids, context=context):
   #              if not sale_obj.freequote_opt_out:
   #                  if sale_obj.no_of_reminder_emails_sent == 4:
   #                         continue
   #                  if sale_obj.no_of_days in ['7 days','14 days','21 days','28 days']:
   #                      no_of_reminder_emails_sent = sale_obj.no_of_reminder_emails_sent  + 1
   #                      self.write(cr,uid,ids,{'no_of_reminder_emails_sent':no_of_reminder_emails_sent})
   #                      template_id = self.pool.get('email.template').search(cr,uid,[('name','=',"Freequote Reminder Email")])
   #                      if template_id:
   #                          mail_message = self.pool.get('email.template').send_mail(cr,uid,template_id[0],sale_obj.id)
   #         return True


class sale_order_line(models.Model):
       _inherit = "sale.order.line"

       pcexam_voucher_id = fields.Many2one('pcexams.voucher','PCExams Voucher')

       # @api.multi
       # def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False, context=None):
       #  """Prepare the dict of values to create the new invoice line for a
       #     sales order line. This method may be overridden to implement custom
       #     invoice generation (making sure to call super() to establish
       #     a clean extension chain).
       #
       #     :param browse_record line: sale.order.line record to invoice
       #     :param int account_id: optional ID of a G/L account to force
       #         (this is used for returning products including service)
       #     :return: dict of values to create() the invoice line
       #  """
       #  res = {}
       #  if not line.invoiced:
       #      if not account_id:
       #          if line.product_id:
       #              account_id = line.product_id.property_account_income.id
       #              if not account_id:
       #                  account_id = line.product_id.categ_id.property_account_income_categ.id
       #              if not account_id:
       #                  raise ValidationError(_('Error!'),
       #                      _('Please define income account for this product: "%s" (id:%d).') % \
       #                              (line.product_id.name, line.product_id.id,))
       #          else:
       #              prop = self.pool.get('ir.property').get(cr, uid,
       #                      'property_account_income_categ', 'product.category',
       #                      context=context)
       #              account_id = prop and prop.id or False
       #      uosqty = self._get_line_qty(cr, uid, line, context=context)
       #      uos_id = self._get_line_uom(cr, uid, line, context=context)
       #      pu = 0.0
       #      if uosqty:
       #          pu = round(line.price_unit * line.product_uom_qty / uosqty,
       #                  self.pool.get('decimal.precision').precision_get(cr, uid, 'Product Price'))
       #      fpos = line.order_id.fiscal_position or False
       #      account_id = self.pool.get('account.fiscal.position').map_account(cr, uid, fpos, account_id)
       #      if not account_id:
       #          raise ValidationError(_('Error!'),
       #                      _('There is no Fiscal Position defined or Income category account defined for default properties of Product categories.'))
       #      res = {
       #          'name': line.name,
       #          'sequence': line.sequence,
       #          'origin': line.order_id.name,
       #          'account_id': account_id,
       #          'price_unit': pu,
       #          'event_id':line.event_id and line.event_id.id or False,
       #          'quantity': uosqty,
       #          'discount': line.discount,
       #          'uos_id': uos_id,
       #          'product_id': line.product_id.id or False,
       #          'invoice_line_tax_id': [(6, 0, [x.id for x in line.tax_id])],
       #          'account_analytic_id': line.order_id.project_id and line.order_id.project_id.id or False,
       #          'pcexam_voucher_id':line.pcexam_voucher_id and line.pcexam_voucher_id.id
       #
       #      }
       #
       #  return res


class res_partner(models.Model):
    _inherit = 'res.partner'

    examwritten = fields.Selection([('1', 'Yes'), ('2', 'No')], "Ever Written PC Exam Before?")
    dob = fields.Date('Date of Birth')
    prof_body_id = fields.Char("Prof Body Student ID",size=56)
    student_company = fields.Char("Students Company",size=256)
    prof_password = fields.Char("Prof Body Login Password",size=56)


class cancel_reason(models.AbstractModel):
    _name="cancel.reason"

    reason = fields.Selection([('non_payment','Non Payment'),('not_reg_prof_body','Not Registered on Professional Body Exam Register'),('not_attend','Non Attendance')],"Reason for Cancellation",required=True)
    #
    # @api.multi
    # def registration_cancel(self,cr,uid,ids, context=None):
    #     self.pool.get('event.registration').button_reg_cancel(cr, uid, context.get('active_ids', []), context=context)
    #     return {'type': 'ir.actions.act_window_close'}


class account_invoice(models.Model):
    _inherit = "account.invoice"

    payu_reference = fields.Char('PayU Reference', size=256)
    payu_transaction_id = fields.Char('PayU Transaction Number', size=256)

    # @api.multi
    # def invoice_pay_customer(self, cr, uid, ids, context=None):
    #     if not ids: return []
    #     dummy, view_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'account_voucher', 'view_vendor_receipt_dialog_form')
    #
    #     inv = self.browse(cr, uid, ids[0], context=context)
    #     return {
    #         'name':_("Pay Invoice"),
    #         'view_mode': 'form',
    #         'view_id': view_id,
    #         'view_type': 'form',
    #         'res_model': 'account.voucher',
    #         'type': 'ir.actions.act_window',
    #         'nodestroy': True,
    #         'target': 'new',
    #         'domain': '[]',
    #         'context': {
    #             'payment_expected_currency': inv.currency_id.id,
    #             'default_partner_id': self.pool.get('res.partner')._find_accounting_partner(inv.partner_id).id,
    #             'default_amount': inv.type in ('out_refund', 'in_refund') and -inv.residual or inv.residual,
    #             'default_reference': inv.name,
    #             'close_after_process': True,
    #             'invoice_type': inv.type,
    #             'invoice_id': inv.id,
    #             'default_type': inv.type in ('out_invoice','out_refund') and 'receipt' or 'payment',
    #             'type': inv.type in ('out_invoice','out_refund') and 'receipt' or 'payment',
    #             'default_name':inv.campus.name or False
    #         }
    #     }
    #
    # @api.multi
    # def confirm_paid(self, cr, uid, ids, context=None):
    #
    #     if context is None:
    #         context = {}
    #     self.write(cr, uid, ids, {'state':'paid'}, context=context)
    #     for invoice in self.browse(cr, uid, ids, context=context):
    #           if invoice.sale_order_id and invoice.sale_order_id.pc_exam:
    #                     self.send_confirmation_email(cr,uid,ids,context)
    #           event_reg_id = self.pool.get('event.registration').search(cr,uid,[('origin','=',invoice.sale_order_id.name)])
    #           self.pool.get('event.registration').registration_open(cr,uid,event_reg_id,context)
    #     return True
    #
    # @api.multi
    # def send_confirmation_email(self,cr,uid,ids,context):
    #        for invoice in self.browse(cr, uid, ids, context=context):
    #                 template_id = self.pool.get('email.template').search(cr,uid,[('name','=',"Invoice - Confirmation")])
    #                 if template_id:
    #                     mail_message = self.pool.get('email.template').send_mail(cr,uid,template_id[0],invoice.id)
    #        return True
    #
    # @api.multi
    # def invoice_print(self, cr, uid, ids, context=None):
    #     '''
    #     This function prints the invoice and mark it as sent, so that we can see more easily the next step of the workflow
    #     '''
    #     assert len(ids) == 1, 'This option should only be used for a single id at a time.'
    #     self.write(cr, uid, ids, {'sent': True}, context=context)
    #     datas = {
    #          'ids': ids,
    #          'model': 'account.invoice',
    #          'form': self.read(cr, uid, ids[0], context=context)
    #     }
    #     return {
    #         'type': 'ir.actions.report.xml',
    #         'report_name': 'account_invoice_enrollment',
    #         'datas': datas,
    #         'nodestroy' : True
    #     }


class account_invoice_line(models.Model):
    _inherit = "account.invoice.line"

    event_id = fields.Many2one('event.event',"Event")
    pcexam_voucher_id = fields.Many2one('pcexams.voucher','PCExams Voucher')