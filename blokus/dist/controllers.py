import pygame
import events as e
import objects as o

class MouseController:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
    def Notify(self, event):
        if isinstance(event, e.PygameEvent):
            event = event.ev
            ev = None
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mpos = pygame.mouse.get_pos()
                    csize = o.board.csize
                    if mpos <= (o.board.w*csize, o.board.h*csize):
                        pos = (mpos[0]/csize,mpos[1]/csize)
                        ev = e.MovePiece(None, pos)
                    else:
                        for p in o.players.pieces:
                            r = p[0].get_rect()
                            r.move_ip(p[0].get_abs_offset())
                            if r.collidepoint(mpos):
                                ev = e.SwitchPiece(p[1],p[2])
                                break
            if ev:
                self.evManager.Post(ev)

class KeyboardController:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
    def Notify(self, event):
        if isinstance(event, e.PygameEvent):
            event = event.ev
            ev = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    ev = e.RotPiece("rotCW")
                elif event.key == pygame.K_LSHIFT:
                    ev = e.RotPiece("flip")
                elif event.key == pygame.K_ESCAPE:
                    ev = e.ResignEvent()
                elif event.key in { pygame.K_KP_ENTER, pygame.K_RETURN }:
                    ev = e.PlacePiece()
            if ev:
                self.evManager.Post(ev)

class TickController:
    def __init__(self, evManager):
        self.evManager = evManager
        self.evManager.RegisterListener(self)
        self.on = True

    def run(self):
        while self.on:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.evManager.Post(e.QuitEvent())
                else:
                    self.evManager.Post(e.PygameEvent(event))
            self.evManager.Post(e.TickEvent())
    def Notify(self, event):
        if isinstance(event, e.QuitEvent):
            self.on = False
