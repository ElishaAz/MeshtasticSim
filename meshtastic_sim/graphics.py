from typing import Callable

import pyglet
from pyglet.window import mouse

from meshtastic_sim import Simulator, Node


_NODE_RADIUS = 7

class Graphics:
    def __init__(self, simulator: Simulator, create_node: Callable[[tuple[float, float]], Node], scale: float,
                 step_interval: float = 1):
        self.simulator = simulator
        self.create_node = create_node
        self.scale = scale
        self.step_interval = step_interval

        self.nodes: dict[Node, tuple[int, int]] = dict()

        self.node_shapes: dict[Node, pyglet.shapes.Circle] = dict()

        self.simulation_shapes: list[pyglet.shapes.ShapeBase] = []

        self.mode = "create"

    def _add_node(self, x, y):
        node = self.create_node((x * self.scale, y * self.scale))
        self.nodes[node] = (x, y)
        self.node_shapes[node] = pyglet.shapes.Circle(x, y, _NODE_RADIUS)
        print(x, y)
        self.simulator.add_node(node)

    def _start_simulation(self):
        self.mode = "simulate"
        self.simulator.start()
        pyglet.clock.schedule_interval(self._do_step, self.step_interval)
        self._do_step(1)

    def _stop_simulation(self):
        self.mode = "create"
        pyglet.clock.unschedule(self._do_step)

    def _do_step(self, dt: float):
        state = self.simulator.do_step()
        self.step_label.text = F"Step {state.step}"

        self.simulation_shapes.clear()
        for node in state.sent_messages.keys():
            (x, y) = self.nodes[node]
            self.simulation_shapes.append(
                pyglet.shapes.Arc(x, y, node.radius / self.scale, thickness=5, color=(255, 0, 0, 255)))

        for node in state.received_messages.keys():
            (x, y) = self.nodes[node]
            self.simulation_shapes.append(pyglet.shapes.Circle(x, y, _NODE_RADIUS, color=(0, 255, 0, 255)))

    def _create(self):
        window = pyglet.window.Window(caption="Meshtastic Sim")

        self.step_label = pyglet.text.Label('Step', 50, 50, font_size=36, color=(255, 255, 255, 255))
        start_button_text = pyglet.text.Label('Start', x=30, y=window.height - 60, font_size=20,
                                              font_name='Times New Roman',
                                              anchor_x='left', anchor_y='bottom', color=(0, 250, 0, 255))
        start_button_rect = pyglet.shapes.RoundedRectangle(x=start_button_text.x - 2, y=start_button_text.y - 2,
                                                           width=60, height=36, radius=2)

        @window.event
        def on_key_press(symbol, modifiers):
            pass

        @window.event
        def on_mouse_press(x, y, button, modifiers):
            if button == mouse.LEFT:
                if self.mode == "create":
                    if (x, y) in start_button_rect:
                        start_button_text.text = "Stop"
                        start_button_text.color = (255, 0, 0, 255)
                        self._start_simulation()
                    else:
                        self._add_node(x, y)
                elif self.mode == "simulate":
                    if (x, y) in start_button_rect:
                        self._stop_simulation()
                        start_button_text.text = "Start"
                        start_button_text.color = (0, 250, 0, 255)

            elif button == mouse.RIGHT:
                if self.mode == "create":
                    for node, (nx, ny) in list(self.nodes.items()):
                        if abs(nx - x) < _NODE_RADIUS and abs(ny - y) < _NODE_RADIUS:
                            self.simulator.remove_node(node)
                            del self.nodes[node]
                            del self.node_shapes[node]
                            break

        @window.event
        def on_draw():
            window.clear()

            for shape in self.node_shapes.values():
                shape.draw()

            start_button_rect.draw()
            start_button_text.draw()

            if self.mode == "simulate":
                for shape in self.simulation_shapes:
                    shape.draw()

                self.step_label.draw()

    def main(self):
        self._create()
        pyglet.app.run()
