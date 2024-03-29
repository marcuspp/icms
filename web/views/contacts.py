from django.db import transaction
from django.shortcuts import render
from web.base.views import PostActionMixin
from web.models import User, Role
from .user import search_people
import logging

logger = logging.getLogger(__name__)


class ContactsManagementMixin(PostActionMixin):
    def _remove_from_session(self, name, default=None):
        "Remvove data from session and return"
        value = self.request.session.pop(name, default)
        logger.debug('Removed from session: {name=%s, value=%s} ', name, value)
        return value

    def _get_post_parameter(self, name):
        return self.request.POST.get(name)

    def _get_post_parameter_as_list(self, name):
        return self.request.POST.getlist(name)

    def _add_to_session(self, name, value):
        "Add data to session"
        self.request.session[name] = value
        logger.debug('Saved to session: {name=%s, value=%s} ', name, value)

    def _get_users_by_ids(self, id_list=[]):
        return list(User.objects.filter(pk__in=id_list))

    def _get_role_members(self, roles):
        role_members = {}
        for role in roles:
            members = []
            for user in list(role.user_set.all()):
                members.append(user)
            role_members[str(role.id)] = members

        return role_members

    def _extract_role_members(self):
        role_members = {}
        for key in self.request.POST:
            if ('role_members_') in key:
                members = self.request.POST.getlist(key)
                role_id = key.replace('role_members_', '')
                role_members[role_id] = members
        return role_members

    def _fetch_role_members(self, role_members=None):
        "Read role members from database"
        result = {}
        members = role_members or self._extract_role_members()
        for role_id, user_ids in members.items():
            logger.debug('Role: %s, Members: %s', role_id, user_ids)
            result[role_id] = self._get_users_by_ids(user_ids)
        logger.debug('Fetched role members: %s', result)
        return result

    def _get_roles(self, object):
        if not object.id:  # New object
            return Role.objects.none()

        return object.roles.all()

    def _get_data(self, object):
        param = self._get_post_parameter_as_list
        roles = self._get_roles(object)
        members = self._get_users_by_ids(param('members'))
        role_members = self._fetch_role_members()
        return {
            'members': members,
            'roles': roles,
            'role_members': role_members
        }

    def _get_initial_data(self, object):
        if not object.id:  # New Object
            return {}

        roles = object.roles.all()
        # TODO: might be slow, use Django api to fetch related efficientl
        return {
            'members': object.members.all(),
            'roles': roles,
            'role_members': self._get_role_members(roles)
        }

    def _save_to_session(self, role_id=None, pk=None):
        put = self._add_to_session
        param = self._get_post_parameter_as_list
        form_data = self.get_form(self.request.POST, pk).data
        put('form', form_data)
        put('members', param('members'))
        put('role_members', self._extract_role_members())
        if role_id:
            put('add_to_role', role_id)

    def _restore_from_session(self, new_members=[], pk=None):
        _pop = self._remove_from_session
        form_data = _pop('form')
        form = self.get_form(data=form_data, pk=pk)
        users = self._get_users_by_ids(_pop('members', []))
        role_members = _pop('role_members', {})
        role_id = _pop('add_to_role')
        if role_id:
            members = role_members.get(str(role_id)) or []
            new_members.extend(members)
            role_members[str(role_id)] = new_members
            logger.debug('Role members: %s', role_members)
        role_members = self._fetch_role_members(role_members)
        new_members = self._get_users_by_ids(new_members)
        for user in users:
            if user not in new_members:
                new_members.append(user)
        return {
            'form': form,
            'contacts': {
                'members': new_members,
                'roles': self._get_roles(form.instance),
                'role_members': role_members
            }
        }

    def _render(self, context={}):
        return render(self.request, self.template_name, context)

    def get_form(self, data=None, pk=None):
        logger.debug('Getting contacts for object pk: %s', pk)
        instance = None
        if pk:
            instance = super().get_object()

        return super().get_form_class()(data, instance=instance)

    def get(self, request, pk=None):
        "Initial get request"
        self._remove_from_session(request)  # clear session data if exists
        form = self.get_form(pk=pk)
        return self._render({
            'contacts': self._get_initial_data(form.instance),
            'form': form
        })

    def add_member(self, request, pk=None):
        add_to_role = request.POST.get('add_to_role', None)
        self._save_to_session(add_to_role, pk)
        return search_people(request)

    def add_people(self, request, pk=None):
        # Handles new members added on search users
        selected_users = self._get_post_parameter_as_list('selected_items')
        data = self._restore_from_session(selected_users, pk=pk)
        logger.debug('Members added to object pk: %s', pk)
        return self._render(data)

    def _save_members(self, object):
        members = set(self._get_post_parameter_as_list('members'))
        object.members.clear()
        for member_id in members:
            object.members.add(member_id)

    def _save_role_members(self, object):
        role_members = self._extract_role_members()
        for role in self._get_roles(object):
            members = role_members.get(str(role.id), [])
            role.user_set.clear()
            for user_id in members:
                role.user_set.add(user_id)

    @transaction.atomic
    def save(self, request, pk=None):
        logger.debug('Save: %s', pk)
        form = self.get_form(request.POST, pk)
        if not form.is_valid():  # render back to display errors
            return self._render({
                'contacts': self._get_data(form.instance),
                'form': form
            })
        object = form.save()
        self._save_members(object)
        self._save_role_members(object)
        return self.get(request, pk)
