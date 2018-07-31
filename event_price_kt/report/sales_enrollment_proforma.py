# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

# import time
# from openerp.report import report_sxw
#
# class sales_proforma_enrollment_kt(report_sxw.rml_parse):
#     def __init__(self, cr, uid, name, context):
#         super(sales_proforma_enrollment_kt, self).__init__(cr, uid, name, context=context)
#         self.localcontext.update({
#             'time': time,
#             'get_terms':self.get_terms,
#             'get_max':self.get_max,
#             'get_discount':self.get_discount,
#         })
#
#     def get_max(self):
#
#         discount = 0
#         max_discount_id = self.pool.get('event.max.discount').search(self.cr,self.uid,[])
#         if max_discount_id:
#             max_discount = self.pool.get('event.max.discount').browse(self.cr,self.uid,max_discount_id)
#
#             for discount1 in max_discount:
#                 discount = discount1.max_discount
#         return discount
#
#     def get_terms(self,event_type,context=None):
#         data = []
#         type_id = self.pool.get('event.type').search(self.cr,self.uid,[('name','=',event_type)])
#         if type_id:
#                discount_ids =  self.pool.get('event.discount').search(self.cr,self.uid,[('event_type_id','=',type_id)])
#                if discount_ids:
#                    result =  self.pool.get('event.discount').browse(self.cr,self.uid,discount_ids)
#                    return result
#         return data
#
#     def get_discount(self,disc_id,sale_id):
#         data = []
#         if disc_id and sale_id:
#              sale_order = self.pool.get('sale.order').browse(self.cr,self.uid,sale_id)
#              for id1 in sale_order.discount_type_ids:
#                  data.append(id1.id)
#              if disc_id in data:
#                 return "Yes"
#              else:
#                 return "No"
#
#         return "Yes"
#
#
# report_sxw.report_sxw(
#     'report.sales_proforma_enrollment',
#     'sale.order',
#     'addons/event_price_kt/report/sales_enrollment_proforma.rml',
#     parser=sales_proforma_enrollment_kt, header=False
# )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

