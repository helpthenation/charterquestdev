# -*- coding: utf-8 -*-

from odoo import fields, models, api,  _
from datetime import date, datetime, timedelta


class event_discounts(models.Model):
    _name = "event.discount"

    name = fields.Char("Name", size=56)
    discount = fields.Float("Discount %")
    event_type_id = fields.Many2one('event.type', "Event Type")
    description = fields.Text("Description")
    order_id = fields.Many2one('sale.order', 'Order Reference', required=True, ondelete='cascade', select=True, readonly=True, states={'draft':[('readonly',False)]})
    condition = fields.Text("Conditions")


class event_max_discount(models.Model):
    _name = "event.max.discount"

    date = fields.Date(string='Date', default=fields.Date.context_today)
    max_discount = fields.Float("Max Discount %",help="Maximum discount allowed on event registration in Portal")


class sale_order(models.Model):
    _inherit = 'sale.order'

    # @api.model
    # def send_early_bird_discount_email(self,cr,uid,context=None):
    #       """ This Function is used to send the Early Bird Discount
    #       Expiry Notification to Student."""
    #
    #       today = datetime.today()
    #       this_first = date(today.year, today.month, 1)
    #       prev_end = this_first - timedelta(days=3)
    #       prev_first = date(prev_end.year, prev_end.month, 1)
    #       month = today.strftime('%m')
    #       sale_ids = self.search(cr,uid,[('state','=','draft'),('create_date','>=',str(prev_first)),('create_date','<=',str(prev_end)),('affiliation','=','1')])
    #       #sale_ids = [1937]
    #
    #       for sale_id in sale_ids:
    #           sale_obj = self.browse(cr,uid,sale_id)
    #           list = []
    #           if sale_obj.discount_type_ids:
    #              discount = 0.0
    #              for event_obj in sale_obj.discount_type_ids:
    #                  max_disc = self.pool.get('event.discount').search(cr,uid,[('name','=','Early Bird Discount')])
    #                  max_discount_id = max_disc and max_disc[0] or False
    #                  if event_obj.id == max_discount_id:
    #                       template_id = self.pool.get('email.template').search(cr,uid,[('name','=',"Early Bird DISCOUNT EXPIRY NOTICE")])
    #                       if template_id:
    #                            mail_message = self.pool.get('email.template').send_mail(cr,uid,template_id[0],sale_obj.id)
    #
    #       return True
    #
    # @api.model
    # def get_early_bird_discount(self,cr,uid,context=None):
    #       today = datetime.today()
    #       this_first = date(today.year, today.month, 1)
    #       prev_end = this_first - timedelta(days=1)
    #       prev_first = date(prev_end.year, prev_end.month, 1)
    #       month = today.strftime('%m')
    #       sale_ids = self.search(cr,uid,[('state','=','draft'),('create_date','>=',str(prev_first)),('create_date','<=',str(prev_end)),('affiliation','=','1')])
    #
    #       for sale_id in sale_ids:
    #           sale_obj = self.browse(cr,uid,sale_id)
    #           list = []
    #           if sale_obj.discount_type_ids:
    #              discount = 0.0
    #              for event_obj in sale_obj.discount_type_ids:
    #                  max_disc = self.pool.get('event.discount').search(cr,uid,[('name','=','Early Bird Discount'),('event_type_id','=',sale_obj.prof_body.id)])
    #                  max_discount_id = max_disc and max_disc[0] or False
    #                  if event_obj.id != max_discount_id:
    #                      list.append(event_obj.id)
    #                      discount += event_obj.discount
    #              self.write(cr,uid,sale_id,{'discount_type_ids':[(6,0,list)],'discount':discount})
    #              message = self.pool.get('mail.message')
    #              if sale_obj.message_ids[0]:
    #                 message.create(cr, uid, {
    #                               'res_id': sale_obj.message_ids[0].res_id,
    #                                'parent_id':sale_obj.message_ids[0].id,
    #                                'subject' : 'Early Bird Discount Removed from Quote',
    #                                'model':'sale.order',
    #                                'body':'Early Bird Discount Removed from Quote'
    #                        }, context)
    #
    #       return True
    #
    # @api.model
    # def send_early_settlement_discount_email(self,cr,uid,context=None):
    #       today = date.today()
    #       sale_ids = self.search(cr,uid,[('state','=','draft'),('affiliation','=','1')])
    #     #  sale_ids = [1937]
    #       for sale_id in sale_ids:
    #           sale_obj = self.browse(cr,uid,sale_id)
    #           list = []
    #           createdate = datetime.strptime(sale_obj.create_date,"%Y-%m-%d %H:%M:%S")
    #           after7_days = today - createdate.date()
    #           if after7_days.days == 5:
    #              if sale_obj.discount_type_ids:
    #                  discount = 0.0
    #                  for event_obj in sale_obj.discount_type_ids:
    #                      max_disc = self.pool.get('event.discount').search(cr,uid,[('name','=','Early Settlement Discount'),('event_type_id','=',sale_obj.prof_body.id)])
    #                      max_discount_id = max_disc and max_disc[0] or False
    #                      if event_obj.id == max_discount_id:
    #                          template_id = self.pool.get('email.template').search(cr,uid,[('name','=',"Early Settelement DISCOUNT EXPIRY NOTICE")])
    #                          if template_id:
    #                              mail_message = self.pool.get('email.template').send_mail(cr,uid,template_id[0],sale_obj.id)
    #
    #       return True
    #
    # @api.model
    # def get_early_settlement_discount(self,cr,uid,context=None):
    #       today = date.today()
    #       sale_ids = self.search(cr,uid,[('state','=','draft'),('affiliation','=','1')])
    #       for sale_id in sale_ids:
    #           sale_obj = self.browse(cr,uid,sale_id)
    #           list = []
    #           createdate = datetime.strptime(sale_obj.create_date,"%Y-%m-%d %H:%M:%S")
    #           after7_days = today - createdate.date()
    #           if after7_days.days > 7:
    #              if sale_obj.discount_type_ids:
    #                  discount = 0.0
    #                  for event_obj in sale_obj.discount_type_ids:
    #                      max_disc = self.pool.get('event.discount').search(cr,uid,[('name','=','Early Settlement Discount'),('event_type_id','=',sale_obj.prof_body.id)])
    #                      max_discount_id = max_disc and max_disc[0] or False
    #                      if event_obj.id != max_discount_id:
    #                          list.append(event_obj.id)
    #                          discount += event_obj.discount
    #                  self.write(cr,uid,sale_id,{'discount_type_ids':[(6,0,list)],'discount':discount})
    #                  message = self.pool.get('mail.message')
    #                  if sale_obj.message_ids[0]:
    #                       message.create(cr, uid, {
    #                               'res_id': sale_obj.message_ids[0].res_id,
    #                                'parent_id':sale_obj.message_ids[0].id,
    #                                'subject' : 'Early Settlement Discount Removed from Quote',
    #                                'model':'sale.order',
    #                                'body':'Early Settlement Discount Removed from Quote'
    #                        }, context)
    #       return True
    #
    # @api.multi
    # def _get_default_discount(self, cr, uid, context=None):
    #
    #       max_disc = self.pool.get('event.discount').search(cr,uid,[('name','=','Early Bird Discount')])
    #       max_discount_id = max_disc and max_disc[0] or False
    #       result = [(6, 0, [max_discount_id])]
    #       return result

         # max_disc_obj = self.pool.get('event.max.discount').browse(cr,uid,max_disc) 
         # discount = max_disc_obj.max_discount

    discount_type_ids = fields.Many2many('event.discount',"event_discount_type_salei",'order_id','discount_type_id',"Discount Types")
    discount = fields.Float("Discount %")
      
    _defaults = {
    #     'discount_type_ids': _get_default_discount,
    }

    # @api.multi
    # def onchange_discount_type(self,cr,uid,ids,discount_type_id,context=None):
    #
    #       if not discount_type_id:
    #             return {'values':{'discount':0.0}}
    #
    #       event_discount = self.pool.get('event.discount')
    #
    #       if discount_type_id:
    #          discount_type_id = discount_type_id[0][2]
    #       event_discount_obj = event_discount.browse(cr,uid,discount_type_id)
    #       discount = 0.0
    #
    #
    #       if isinstance(event_discount_obj,list):
    #         for obj in event_discount_obj:
    #             discount += obj.discount
    #       else:
    #         for obj in event_discount_obj:
    #            discount += obj.discount
    #
    #       max_disc = False
    #       today = str(date.today())
    #       event_max_discount_ids = self.pool.get('event.max.discount').search(cr,uid,[('date','<=',today)])
    #
    #       if len(event_max_discount_ids) >= 2:
    #            event_max_discount_ids = [max(event_max_discount_ids)]
    #       max_disc = self.pool.get('event.max.discount').browse(cr,uid,event_max_discount_ids[0]).max_discount
    #       if max_disc and discount > max_disc:
    #           discount = max_disc
    #       return {'value':{'discount':discount}}
    #
    # @api.multi
    # def write(self, cr, uid, ids, vals, context=None):
    #       if vals.get('discount',False) and vals['discount'] >= 0.0:
    #            order_id = ids
    #            if isinstance(ids,int):
    #                 order_id = [ids]
    #            order_line_ids = self.pool.get('sale.order.line').search(cr,uid,[('order_id','=',order_id)])
    #            line_ids = []
    #            for obj in self.pool.get('sale.order.line').browse(cr,uid,order_line_ids):
    #                if not obj.product_id.fee_ok:
    #                      line_ids.append(obj.id)
    #            self.pool.get('sale.order.line').write(cr,uid,line_ids,{'discount':vals['discount']})
    #
    #       return super(sale_order, self).write(cr, uid, ids, vals, context)

# class sale_order_line(models.Model):
#
#      _inherit = "sale.order.line"
#
#      @api.multi
#      def create(self, cr, uid, vals, context=None):
#          if vals.get('product_id',False):
#               if not self.pool.get('product.product').browse(cr,uid,vals['product_id']).fee_ok:
#                 discount = self.pool.get('sale.order').browse(cr,uid,vals['order_id']).discount
#                 vals['discount'] = discount
#                 return super(sale_order_line, self).create(cr, uid, vals, context)


class product_product(models.Model):
    _inherit = 'product.product'

    does_not_apply = fields.Selection([('return_student','Returning Student'),('new_student','New Student')],'Does not apply to')
    pcexam_voucher = fields.Boolean('PC Exam Voucher')
    no_vouchers = fields.Integer('No of Vouchers')
    voucher_value = fields.Float('Voucher Value')