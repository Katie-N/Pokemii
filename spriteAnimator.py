import pygame

class SpriteAnimator:
    def __init__(self, spritesheet: pygame.Surface, frame_width: int, frame_height: int,
                 num_frames: int, row: int = 0, frame_duration: int = 5, loop: bool = True):
        self.spritesheet = spritesheet
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.num_frames = num_frames
        self.row = row
        self.frame_duration = frame_duration
        self.loop = loop

        self.frames = self.extract_frames()
        self.current_frame_index = 0
        self.tick = 0

    def extract_frames(self):
        frames = []
        for i in range(self.num_frames):
            x = i * self.frame_width
            y = self.row * self.frame_height
            frame = self.spritesheet.subsurface(pygame.Rect(x, y, self.frame_width, self.frame_height))
            frames.append(frame)
        return frames

    def update(self):
        self.tick += 1
        if self.tick >= self.frame_duration:
            self.tick = 0
            self.current_frame_index += 1
            if self.current_frame_index >= self.num_frames:
                if self.loop:
                    self.current_frame_index = 0
                else:
                    self.current_frame_index = self.num_frames - 1

    def get_frame(self):
        return self.frames[self.current_frame_index]

    def reset(self):
        self.current_frame_index = 0
        self.tick = 0
