# app/services/rbac.py
from app.models.user import UserRole, ROLE_PERMISSIONS, Permission

class RBACService:
    @staticmethod
    def has_permission(user_role: str, permission: str) -> bool:
        """
        Check if a user role has a specific permission
        """
        try:
            role_enum = UserRole(user_role)
            return permission in ROLE_PERMISSIONS.get(role_enum, [])
        except ValueError:
            # If role is not valid, deny permission
            return False
    
    @staticmethod
    def has_any_permission(user_role: str, permissions: list) -> bool:
        """
        Check if a user role has any of the specified permissions
        """
        try:
            role_enum = UserRole(user_role)
            role_permissions = ROLE_PERMISSIONS.get(role_enum, [])
            return any(permission in role_permissions for permission in permissions)
        except ValueError:
            # If role is not valid, deny permission
            return False
    
    @staticmethod
    def has_all_permissions(user_role: str, permissions: list) -> bool:
        """
        Check if a user role has all of the specified permissions
        """
        try:
            role_enum = UserRole(user_role)
            role_permissions = ROLE_PERMISSIONS.get(role_enum, [])
            return all(permission in role_permissions for permission in permissions)
        except ValueError:
            # If role is not valid, deny permission
            return False
    
    @staticmethod
    def get_role_permissions(user_role: str) -> list:
        """
        Get all permissions for a user role
        """
        try:
            role_enum = UserRole(user_role)
            return ROLE_PERMISSIONS.get(role_enum, [])
        except ValueError:
            # If role is not valid, return empty list
            return []
    
    @staticmethod
    def is_super_admin(user_role: str) -> bool:
        """
        Check if user is super admin
        """
        return user_role == UserRole.ADMIN
    
    @staticmethod
    def can_manage_users(user_role: str) -> bool:
        """
        Check if user can manage users (excluding super admin management)
        """
        return RBACService.has_permission(user_role, Permission.CREATE_USER)
    
    @staticmethod
    def can_manage_admins(user_role: str) -> bool:
        """
        Check if user can manage admins (only super admin can)
        """
        return RBACService.is_super_admin(user_role)
    
    @staticmethod
    def can_access_system_config(user_role: str) -> bool:
        """
        Check if user can access system configuration
        """
        return RBACService.has_permission(user_role, Permission.CONFIGURE_SYSTEM)
    
    @staticmethod
    def can_manage_modules(user_role: str) -> bool:
        """
        Check if user can manage modules
        """
        return RBACService.has_permission(user_role, Permission.MANAGE_MODULES)
    
    @staticmethod
    def can_access_all_data(user_role: str) -> bool:
        """
        Check if user can access all data
        """
        return RBACService.has_permission(user_role, Permission.ACCESS_ALL_DATA)
    
    @staticmethod
    def can_run_reports(user_role: str) -> bool:
        """
        Check if user can run reports
        """
        return RBACService.has_permission(user_role, Permission.RUN_REPORTS)
    
    @staticmethod
    def can_manage_academics(user_role: str) -> bool:
        """
        Check if user can manage academic data
        """
        return RBACService.has_any_permission(user_role, [
            Permission.MANAGE_CLASSES,
            Permission.MANAGE_SUBJECTS,
            Permission.MANAGE_TIMETABLES,
            Permission.MANAGE_GRADES,
            Permission.MANAGE_ATTENDANCE
        ])
    
    @staticmethod
    def can_manage_finance(user_role: str) -> bool:
        """
        Check if user can manage financial data
        """
        return RBACService.has_any_permission(user_role, [
            Permission.MANAGE_FEES,
            Permission.MANAGE_PAYMENTS,
            Permission.MANAGE_EXPENSES
        ])
    
    @staticmethod
    def can_communicate(user_role: str) -> bool:
        """
        Check if user can communicate
        """
        return RBACService.has_any_permission(user_role, [
            Permission.SEND_ANNOUNCEMENTS,
            Permission.SEND_MESSAGES
        ])
    
    @staticmethod
    def can_view_own_data(user_role: str) -> bool:
        """
        Check if user can view their own data
        """
        return RBACService.has_any_permission(user_role, [
            Permission.VIEW_OWN_PROFILE,
            Permission.VIEW_OWN_ACADEMICS,
            Permission.VIEW_OWN_ATTENDANCE,
            Permission.VIEW_OWN_SCHEDULE
        ])
    
    @staticmethod
    def can_update_own_data(user_role: str) -> bool:
        """
        Check if user can update their own data
        """
        return RBACService.has_permission(user_role, Permission.UPDATE_OWN_PROFILE)

# Global RBAC service instance
rbac_service = RBACService()