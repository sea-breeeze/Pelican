import uiautomation as auto


class UIInspector:

    
    def inspect_window(self, window):
        elements = []

        root = auto.ControlFromHandle(window.getHandle())

        if root is None:
            return elements

        def explore(control, depth):
            if depth > 3:
                return

            try:
                
                rectangle = control.BoundingRectangle

                elements.append({
                    "name": control.Name,
                    "type": control.ControlTypeName,
                    "depth": depth,
                    "left": rectangle.left,
                    "top": rectangle.top,
                    "width": rectangle.width(),
                    "height": rectangle.height(),
                    "control": control
                })

                for child in control.GetChildren():
                    explore(child, depth + 1)

            except Exception:
                return

        explore(root, 0)

        return elements

