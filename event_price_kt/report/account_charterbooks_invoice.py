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

import time
from openerp.report import report_sxw
import re

class account_charterbooks_kt(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(account_charterbooks_kt, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
	    'get_terms':self.get_terms,
	    'get_conditions':self.get_conditions,
	    'get_name':self.get_name,
        })

    def get_name(self, record):
        if record.product_id.name == 'Delivery': return record.name
        else: return record.product_id.name    

    def get_terms(self,event_type,context=None):
	data = []
	type_id = self.pool.get('event.type').search(self.cr,self.uid,[('name','=',event_type)])
	if type_id:
	       discount_ids =  self.pool.get('event.discount').search(self.cr,self.uid,[('event_type_id','=',type_id)])
	       if discount_ids:
		   result =  self.pool.get('event.discount').browse(self.cr,self.uid,discount_ids)
		   return result
	return data

    def get_conditions(self):
        terms_id = self.pool.get('terms.conditions').search(self.cr,self.uid,[('type','=ilike','CharterBooks')])
        terms = ''
        if terms_id:
            terms = self.pool.get('terms.conditions').browse(self.cr,self.uid,terms_id[0]).terms_condition
            terms = re.sub('<[^<]+?>', '\n', terms)
        return terms

report_sxw.report_sxw(
    'report.account_invoice_charterbooks',
    'account.invoice',
    'addons/event_price_kt/report/account_charterbooks_invoice.rml',
    parser=account_charterbooks_kt, header=False
)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

