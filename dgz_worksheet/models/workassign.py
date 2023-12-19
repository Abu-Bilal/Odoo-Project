from odoo import models, fields, api,_


class Assigntask(models.Model):
    _name = 'assign.task'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', tracking=True)
    user_id = fields.Many2one('res.users', string='User', tracking=True)
    project_id = fields.Many2one('project.project', string='Project', tracking=True)
    task_id = fields.Many2one('project.task', string='Task', tracking=True)
    status = fields.Selection([('working', 'working'), ('onhold', 'onhold'), ('done', 'done')], string='Status',
                              default='onhold', tracking=True)

    @api.onchange('project_id')
    def _onchange_project(self):
        if self.project_id:
            return {'domain': {'task_id': [('project_id', '=', self.project_id.id)]}}
        else:
            return {'domain': {'task_id': []}}

    @api.onchange('task_id')
    def _onchange_task(self):
        if self.task_id:
            self.project_id = self.task_id.project_id.id

    @api.model
    def get_user_records(self):
        administrator = self.env.user.has_group('dgz_worksheet.ws_administrator')
        tasks = self.search([('status', '!=', 'done')])
        user = {}
        for rec in tasks:
            user_name = rec.user_id.name
            if administrator or rec.user_id.id == self.env.user.id:
                if user_name not in user:
                    user[user_name] = {'user_name': user_name, 'tasks': []}
                user[user_name]['tasks'].append({
                    'name': rec.name or '',
                    'project_id': rec.project_id.name or '',
                    'task_id': rec.task_id.name or '',
                    'status': rec.status or '',
                })
        records = sorted(user.values(), key=lambda x: x['user_name'])
        return records
