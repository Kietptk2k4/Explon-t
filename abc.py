import sys  # Thư viện sys được dùng để truy cập các hàm và biến cụ thể của trình thông dịch Python giúp bạn tương tác với hệ thống, ở đây nó giúp thoát chương trình khi cần thiết sys.exit().
import pygame  # Thư viện pygame được dùng để tạo ra các trò chơi 2D hoặc ứng dụng đồ họa đơn giản.

from pygame.locals import *  # Nhập các hằng số cần thiết từ pygame.locals mà không cần phải ghi pygame. trước chúng (ví dụ: QUIT, K_ESCAPE)

import data.tile_map as tile_map  # type: ignore # Đảm bảo rằng file này tồn tại và có class TileMap
import data.spritesheet_loader as spritesheet_loader # "as spritesheet_loader" dùng để viết ngắn gọn cho "data.spritesheet_loader"

pygame.init()  # Khởi tạo tất cả các module trong thư viện Pygame.
pygame.display.set_caption('Explon\'t')

screen = pygame.display.set_mode((500, 500), 0, 32)  # Tạo một cửa sổ đồ họa kích thước 500x500 pixel.
display = pygame.Surface((250, 250))  # Tạo một bề mặt đồ họa kích thước 250x250 pixel.Đây là một bề mặt phụ, không được hiển thị trực tiếp lên màn hình mà được dùng để vẽ trước các nội dung lên đó. Kích thước của display nhỏ hơn (250, 250 pixel). Sau khi vẽ các nội dung lên display, bề mặt này sẽ được phóng to (scale) và vẽ lại lên screen (màn hình chính).Việc xử lý trên một bề mặt nhỏ sẽ tiêu tốn ít tài nguyên bộ nhớ và CPU hơn.Trong nhiều trò chơi 2D, đồ họa pixel (pixel art) được sử dụng rất nhiều. Với kích thước nhỏ như (250x250), mỗi pixel trên display có thể được phóng to để tạo ra hình ảnh giống như đồ họa pixel lớn hơn trên màn hình. Việc này giúp giữ được sự chi tiết và rõ ràng của pixel art khi hiển thị trên kích thước lớn hơn. Nếu bạn vẽ trực tiếp lên bề mặt lớn (500x500), hiệu ứng pixel art sẽ không được nổi bật và có thể trông không đẹp.Làm việc với display nhỏ hơn cũng giúp bạn kiểm soát tốt hơn việc vẽ, đặc biệt khi cần phóng to hoặc thu nhỏ nội dung. Điều này thường thấy trong các game có camera di chuyển hoặc cần hiệu ứng zoom

TILE_SIZE = 16  # Kích thước của mỗi tile (ô vuông) trong bản đồ.

clock = pygame.time.Clock()  # Quản lý tốc độ khung hình (FPS).

spritesheets,spritesheets_data = spritesheet_loader.load_spritesheets('data/images/spritesheets/') #45->59 trong file spritesheet_loader.py; return dict1[list[list]] chứa các khung tile từ png, dict2 chứa các file python chuyển từ file json

level_map = tile_map.TileMap((TILE_SIZE, TILE_SIZE), display.get_size())  # Đặt tên level_map ám chỉ các map từng level; nó Tạo bản đồ từ class TileMap, gọi hàm init ở class tile_map
level_map.load_map( 'data/maps/map_0.json')# trong file json này có "map": {...},
                                                      #             "off_grid_map": {...},
                                                      #             "all_layers": [...]

for entity in level_map.load_entities():
    print(entity)

scroll = [0,0]

while True:
    display.fill((0, 0, 0))  # Tô đen toàn bộ màn hình.

    scroll[0]+=1

    render_list = level_map.get_visible(scroll)
    for layer in render_list:
        layer_id = layer[0]
        for tile in layer[1]:
            offset = [0,0]
            if tile[1][0] in spritesheets_data:
                tile_id = str(tile[1][1])+';'+str(tile[1][2])
                if tile_id in spritesheets_data[tile[1][0]]:
                    if 'tile_offset' in spritesheets_data[tile[1][0]][tile_id]:
                        offset = spritesheets_data[tile[1][0]][tile_id]['tile_offset']
            img = spritesheet_loader.get_img(spritesheets,tile[1])
            print((tile[0][0] - scroll[0] + offset[0], tile[0][1] - scroll[1]+ offset[1]))
            # if layer_opacity:
            #     if layer_id != current_layer:
            #         img = img.copy()
            #         img.set_alpha(100)
            display.blit(img ,(tile[0][0] - scroll[0] + offset[0], tile[0][1] - scroll[1]+ offset[1]))

    for event in pygame.event.get():  # Lấy tất cả các sự kiện từ hàng đợi sự kiện của Pygame.
        if event.type == pygame.QUIT:  # Kiểm tra xem người dùng có nhấn nút đóng cửa sổ không.
            pygame.quit()  # Đóng tất cả các module Pygame đang hoạt động.
            sys.exit()  # Thoát khỏi chương trình ngay lập tức.
        if event.type == pygame.KEYDOWN:  # Kiểm tra xem người dùng có nhấn một phím bất kỳ không.
            if event.key == pygame.K_ESCAPE:  # Nếu phím ESC được nhấn, thoát chương trình.
                pygame.quit()
                sys.exit()


    screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))     #Thay đổi kích thước bề mặt display để phù hợp với kích thước của màn hình chính screen.(0, 0) có nghĩa là vẽ display từ góc trên bên trái của screen
    pygame.display.update()  # Cập nhật nội dung màn hình.
    clock.tick(60)  # Giới hạn tốc độ khung hình của trò chơi là 60 FPS.
