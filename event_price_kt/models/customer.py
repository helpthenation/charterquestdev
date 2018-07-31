
from odoo import fields, models, api, _
from odoo.tools.translate import _
from odoo import SUPERUSER_ID
from datetime import datetime, timedelta


class res_partner(models.Model):
    _inherit = 'res.partner'

    previous_student = fields.Boolean("Previous Student")
    current_student = fields.Boolean('Current Student')
    student_number = fields.Char('Student No',size=64)
    student_number_allocated = fields.Boolean('Student No Allocated')
    is_campus = fields.Boolean('Is Campus')
    campus_code = fields.Char('Campus Code',size=64)

    # @api.model
    # def get_student_number(self, cr, uid, context=None):
    #     partner_ids = self.search(cr, uid, [])
    #     for partner_id in partner_ids:
    #         partner_obj = self.browse(cr, uid, partner_id)
    #         account_ids = self.pool.get('account.invoice').search(cr, uid, [('partner_id', '=', partner_id),
    #                                                                       ('state', '!=', 'draft'),
    #                                                                       ('sale_order_id.pc_exam', '=', False)])
    #         for account_obj in self.pool.get('account.invoice').browse(cr, uid, account_ids):
    #             if account_obj.payment_ids:
    #                 if partner_obj.event_type_id and account_obj.prof_body.name != 'PC Exam':
    #                     if not partner_obj.student_number:
    #                         number = self.pool.get('ir.sequence').get(cr, uid, 'res.partner') or '/'
    #                         today = datetime.now()
    #                         year = today.strftime('%y')
    #                         if account_obj.campus.campus_code:
    #                             serial_number = account_obj.prof_body.professional_body_code+str(account_obj.campus.campus_code)+str(year)+number
    #                         else:
    #                             serial_number = account_obj.prof_body.professional_body_code+str(year)+number
    #                         partner = self.write(cr,uid,partner_id,{'student_number':serial_number,'student_number_allocated':True})
    #                         template_id = self.pool.get('email.template').search(cr,uid,[('name','=',"Student Number")])
    #                         if template_id:
    #                             mail_message = self.pool.get('email.template').send_mail(cr,uid,template_id[0],partner_id)
    #     return True

    # @api.multi
    # def get_student_status(self,cr,uid,context=None):
    #
    #      account_invoice = self.pool.get('account.invoice')
    #      invoice_ids = account_invoice.search(cr,uid,[('date_invoice','>=','2013-01-01'),('date_invoice','<=','2013-12-31'),('quote_type','=','enrolment'),('sale_order_id.pc_exam','=',False)])
    #      invoice_obj = account_invoice.read(cr,uid,invoice_ids,['partner_id'])
    #      partner_ids_2013 = []
    #      for obj in invoice_obj:
    #          partner_ids_2013.append(obj['partner_id'][0])
    #
    #      self.pool.get('res.partner').write(cr,uid,partner_ids_2013,{'previous_student':True})
    #
    #      invoice_ids = account_invoice.search(cr,uid,[('date_invoice','>=','2014-01-01'),('date_invoice','<=','2014-12-31'),('semester','=',1),('quote_type','=','enrolment'),('sale_order_id.pc_exam','=',False),('partner_id.previous_student','=',False)])
    #      invoice_obj = account_invoice.read(cr,uid,invoice_ids,['partner_id'])
    #      partner_ids_2014 = []
    #      for obj in invoice_obj:
    #          partner_ids_2014.append(obj['partner_id'][0])
    #
    #      self.pool.get('res.partner').write(cr,uid,partner_ids_2014,{'current_student':True})
    #      return True


class res_partner_bank(models.Model):
    _inherit = 'res.partner.bank'

    acc_valid_state = fields.Selection([('pend_v','Pending Validation'),('pend_r','Pending Result'),('valid','Valid'),('invalid','Invalid')],'Validation Status')
    acc_holder_name = fields.Char('Account Holder Name')
