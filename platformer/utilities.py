def draw_img(screen, img, x, y):
    img_rect = img.get_rect(center=(x, y))
    screen.blit(img, img_rect)

