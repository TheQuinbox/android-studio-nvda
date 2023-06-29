import appModuleHandler
from scriptHandler import script
import ui
import api
import controlTypes
from editableText import EditableTextWithoutAutoSelectDetection

class AppModule(appModuleHandler.AppModule):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.role == controlTypes.Role.EDITABLETEXT:
			clsList.insert(0, EnhancedEditableText)

	@script(gesture="kb:nvda+e")
	def script_readStatusBar(self, gesture):
		# We currently use simple children, because the view hierarchy is nasty. Even though, to object nav, the status bar is at the top level of it, according to .children it's not.
		# This is kind of slow, but not slow enough to really matter. If it proves to be a problem, though, I can look into enumerating nested children over and over, although that hardly seems like it would be any better. Certainly not enough to justify the code mess.
		obj = api.getForegroundObject().simpleFirstChild
		while obj is not None:
			if obj.role == controlTypes.Role.STATUSBAR:
				break
			obj = obj.simpleNext
		# Literally every single one of these attributes can be None. I hate it here.
		ui.message("No status line found" if obj is None else getattr(obj.simpleFirstChild, "name", "No status line found"))

class EnhancedEditableText(EditableTextWithoutAutoSelectDetection):
	# This exists because of key commands like F2 or shift+F2 that move your caret, but don't make NVDA speak. Accessibility is hard, I guess.

	__gestures = {
		"kb:f2": "caret_moveByLine",
		"kb:shift+f2": "caret_moveByLine",
	}
