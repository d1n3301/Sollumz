import bpy
from ...sollumz_ui import BasicListHelper, FlagsPanel, draw_list_with_add_remove
from ..properties.ytyp import ArchetypeType
from ..properties.mlo import RoomProperties, PortalProperties, TimecycleModifierProperties
from ..utils import get_selected_archetype, get_selected_room, get_selected_portal, get_selected_tcm
from .archetype import SOLLUMZ_PT_ARCHETYPE_PANEL


class SOLLUMZ_UL_ROOM_LIST(BasicListHelper, bpy.types.UIList):
    bl_idname = "SOLLUMZ_UL_ROOM_LIST"
    item_icon = "CUBE"


class SOLLUMZ_PT_ROOM_PANEL(bpy.types.Panel):
    bl_label = "Rooms"
    bl_idname = "SOLLUMZ_PT_ROOM_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = SOLLUMZ_PT_ARCHETYPE_PANEL.bl_idname

    bl_order = 2

    @classmethod
    def poll(cls, context):
        selected_archetype = get_selected_archetype(context)

        return selected_archetype.type == ArchetypeType.MLO

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        selected_archetype = get_selected_archetype(context)

        list_col = draw_list_with_add_remove(self.layout, "sollumz.createroom", "sollumz.deleteroom",
                                             SOLLUMZ_UL_ROOM_LIST.bl_idname, "", selected_archetype, "rooms", selected_archetype, "room_index")

        list_col.operator("sollumz.createlimboroom")

        row = layout.row()
        row.use_property_split = False
        row.prop(context.scene, "show_room_gizmo")

        if not selected_archetype.asset and context.scene.show_room_gizmo:
            row = layout.row()
            row.alert = True
            row.label(
                text="Gizmo will not appear when no object is linked.")

        selected_room = get_selected_room(context)
        if not selected_room:
            return

        layout.separator()
        for prop_name in RoomProperties.__annotations__:
            if prop_name in ["flags", "id"]:
                continue
            layout.prop(selected_room, prop_name)

        list_col.operator(
            "sollumz.setroomboundsfromselection", icon="GROUP_VERTEX")


class SOLLUMZ_PT_ROOM_FLAGS_PANEL(FlagsPanel, bpy.types.Panel):
    bl_idname = "SOLLUMZ_PT_ROOM_FLAGS_PANEL"
    bl_label = "Room Flags"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = SOLLUMZ_PT_ROOM_PANEL.bl_idname

    @classmethod
    def poll(cls, context):
        return get_selected_room(context) is not None

    def get_flags(self, context):
        selected_room = get_selected_room(context)
        return selected_room.flags


class SOLLUMZ_UL_PORTAL_LIST(BasicListHelper, bpy.types.UIList):
    bl_idname = "SOLLUMZ_UL_PORTAL_LIST"
    item_icon = "OUTLINER_OB_LIGHTPROBE"
    name_editable = False


class SOLLUMZ_PT_PORTAL_PANEL(bpy.types.Panel):
    bl_label = "Portals"
    bl_idname = "SOLLUMZ_PT_PORTAL_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = SOLLUMZ_PT_ARCHETYPE_PANEL.bl_idname
    bl_order = 3

    @classmethod
    def poll(cls, context):
        selected_archetype = get_selected_archetype(context)
        return selected_archetype.type == ArchetypeType.MLO

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        selected_archetype = get_selected_archetype(context)

        list_col = draw_list_with_add_remove(self.layout, "sollumz.createportal", "sollumz.deleteportal",
                                             SOLLUMZ_UL_PORTAL_LIST.bl_idname, "", selected_archetype, "portals", selected_archetype, "portal_index")
        row = list_col.row(align=True)
        row.operator("sollumz.createportalfromselection",
                     text="Create From Vertices", icon="GROUP_VERTEX")
        row.operator("sollumz.updateportalfromselection",
                     text="Update From Vertices")

        row = layout.row()
        row.use_property_split = False
        row.prop(context.scene, "show_portal_gizmo")

        if not selected_archetype.asset and context.scene.show_portal_gizmo:
            row = layout.row()
            row.alert = True
            row.label(text="Gizmo will not appear when no object is linked.")

        selected_portal = get_selected_portal(context)

        if not selected_portal:
            return

        layout.separator()
        for prop_name in PortalProperties.__annotations__:
            if prop_name in ["room_from_index", "room_to_index", "name", "room_from_id", "room_to_id", "flags", "id"]:
                continue

            row = layout.row()
            row.prop(selected_portal, prop_name)

            if prop_name == "room_from_name":
                row.operator("sollumz.setportalroomfrom")
            elif prop_name == "room_to_name":
                row.operator("sollumz.setportalroomto")


class SOLLUMZ_PT_PORTAL_FLAGS_PANEL(FlagsPanel, bpy.types.Panel):
    bl_idname = "SOLLUMZ_PT_PORTAL_FLAGS_PANEL"
    bl_label = "Portal Flags"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = SOLLUMZ_PT_PORTAL_PANEL.bl_idname

    @classmethod
    def poll(cls, context):
        return get_selected_portal(context) is not None

    def get_flags(self, context):
        selected_portal = get_selected_portal(context)
        return selected_portal.flags


class SOLLUMZ_UL_TIMECYCLE_MODIFIER_LIST(BasicListHelper, bpy.types.UIList):
    bl_idname = "SOLLUMZ_UL_TIMECYCLE_MODIFIER_LIST"
    item_icon = "MOD_TIME"


class SOLLUMZ_PT_TIMECYCLE_MODIFIER_PANEL(bpy.types.Panel):
    bl_label = "Timecycle Modifiers"
    bl_idname = "SOLLUMZ_PT_TIMECYCLE_MODIFIER_PANEL"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {"DEFAULT_CLOSED"}
    bl_parent_id = SOLLUMZ_PT_ARCHETYPE_PANEL.bl_idname
    bl_order = 4

    @classmethod
    def poll(cls, context):
        selected_archetype = get_selected_archetype(context)

        return selected_archetype.type == ArchetypeType.MLO

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        selected_archetype = get_selected_archetype(context)

        draw_list_with_add_remove(self.layout, "sollumz.createtimecyclemodifier", "sollumz.deletetimecyclemodifier",
                                  SOLLUMZ_UL_TIMECYCLE_MODIFIER_LIST.bl_idname, "", selected_archetype, "timecycle_modifiers", selected_archetype, "tcm_index")

        selected_tcm = get_selected_tcm(context)

        if not selected_tcm:
            return

        layout.separator()

        for prop_name in TimecycleModifierProperties.__annotations__:
            layout.prop(selected_tcm, prop_name)


class SOLLUMZ_PT_MLO_FLAGS_PANEL(FlagsPanel, bpy.types.Panel):
    bl_idname = "SOLLUMZ_PT_MLO_FLAGS_PANEL"
    bl_label = "MLO Flags"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_parent_id = SOLLUMZ_PT_ARCHETYPE_PANEL.bl_idname

    bl_order = 6

    @classmethod
    def poll(cls, context):
        selected_archetype = get_selected_archetype(context)
        return selected_archetype.type == ArchetypeType.MLO

    def get_flags(self, context):
        selected_archetype = get_selected_archetype(context)
        return selected_archetype.mlo_flags