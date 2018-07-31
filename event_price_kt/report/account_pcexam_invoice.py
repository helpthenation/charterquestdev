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
# from openerp.osv import fields,osv
# from datetime import datetime
# from openerp import tools
# import re
#
# class account_invoice_kt(report_sxw.rml_parse):
#     def __init__(self, cr, uid, name, context):
# 	cr=cr
# 	uid=uid
#         super(account_invoice_kt, self).__init__(cr, uid, name, context=context)
#         self.localcontext.update({
#             'time': time,
#             'get_term':self.get_term,
# 	   # 'date_format':self.date_format,
#         })
#
#     def get_term(self):
#         data = []
#         term_id = self.pool.get('terms.conditions').search(self.cr,self.uid,[('type','=','PC Exams')])
#
#         if term_id:
#              result =  self.pool.get('terms.conditions').browse(self.cr,self.uid,term_id)[0]
#              data1 = result['terms_condition']
#
#              data1 = re.sub('<[^<]+?>', '\n', data1)
#              #data1 = html2text.html2text(data1)
#              return data1
#         return data
# #    def date_format(self,date,context=None):
# #	if date:
# #		try:
# #		    result = str(fields.datetime.context_timestamp(self.cr,self.uid, datetime.strptime(date, tools.DEFAULT_SERVER_DATETIME_FORMAT), context=context)).split('+')[0]
# #		    return result
# #		except:
# #		    return date
#
# report_sxw.report_sxw(
#     'report.account_invoice_pcexams',
#     'account.invoice',
#     'addons/event_price_kt/report/account_pcexam_invoice.rml',
#     parser=account_invoice_kt, header=False
# )
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

