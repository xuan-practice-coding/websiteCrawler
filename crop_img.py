# -*- coding: utf-8 -*-
"""
Created on Wed Aug 25 10:07:50 2021

@author: Xuan Chen (Lydia)
"""

import os
from PIL import Image
from fpdf import FPDF

main_path = 'E://DEI//Crawler_Code//test_dir//lusbrands.com//reviews//'

# subpath = [
    # 'pages_lus-reviews',
    # 'collections_accessories_products_detangle-style-brush',
    # 'collections_accessories_products_lus-flairosol-spray-bottle',
    # 'collections_accessories_products_satin-scarf',
    # 'collections_accessories_products_t-shirt-towel',
    # 'collections_black-label-line_products_deep-conditioner',
    # 'collections_black-label-line_products_hair-perfume',
    # 'collections_black-label-line_products_lus-elixir-oil'
    # 'collections_complete-curl-care-system-for-moisturized-healthy-kinks-coils_products_love-ur-curls-all-in-one-leave-in-for-moisturized-healthy-kinks-coils'
    # 'collections_complete-curl-care-system-for-moisturized-healthy-kinks-coils_products_love-ur-curls-complete-curl-care-for-moisturized-healthy-kinks-coils-1'
    # 'collections_complete-curl-care-system-for-soft-weightless-waves_products_love-ur-curls'
    # 'collections_complete-curl-care-system-for-soft-weightless-waves_products_love-ur-curls-simple-3-step-system-bundle'
    # 'collections_complete-curl-care-system-for-ultra-soft-luxurious-curls_products_love-ur-curls-all-in-one-leave-in-for-super-soft-luxurious-curls'
    # 'collections_complete-curl-care-system-for-ultra-soft-luxurious-curls_products_love-ur-curls-complete-curl-care-for-ultra-soft-luxurious-curls'
    # 'collections_complete-curl-care-system-for-ultra-soft-luxurious-curls_products_love-ur-curls-shampoo'
    # 'collections_complete-curl-care-system-for-ultra-soft-luxurious-curls_products_love-ur-curls-ultra-hydrating-detangling-conditioner'
    # 'collections_lus-1-litres_products_1l-all-in-one-curly'
    # 'collections_lus-1-litres_products_1l-all-in-one-kinky-coily'
    # 'collections_lus-1-litres_products_1l-all-in-one-wavy'
    # 'collections_lus-1-litres_products_1l-gentle-moisturizing-shampoo'
    # 'collections_lus-1-litres_products_1l-hydrating-detangling-conditioner'
    # 'collections_lus-infinity_products_deep-conditioner'
    # 'collections_lus-infinity_products_love-ur-curls'
    # 'collections_lus-infinity_products_love-ur-curls-all-in-one-leave-in-for-moisturized-healthy-kinks-coils'
    # 'collections_lus-infinity_products_love-ur-curls-all-in-one-leave-in-for-super-soft-luxurious-curls'
    # 'collections_lus-infinity_products_love-ur-curls-shampoo'
    # 'collections_lus-infinity_products_love-ur-curls-ultra-hydrating-detangling-conditioner'
    # 'collections_lus-infinity_products_lus-elixir-oil'
    # 'collections_treat-and-repair_products_deep-conditioner'
    # 'products_1l-all-in-one-curly'
    # 'products_1l-all-in-one-kinky-coily'
    # 'products_1l-all-in-one-wavy'
    # 'products_1l-gentle-moisturizing-shampoo'
    # 'products_1l-hydrating-detangling-conditioner'
    # 'products_all-in-one-curly-fragrance-free'
    # 'products_all-in-one-kinky-coily-fragrance-free'
    # 'products_all-in-one-wavy-fragrance-free'
    # 'products_complete-curl-care-for-moisturized-healthy-kinks-coils-fragrance-free'
    # 'products_complete-curl-care-for-soft-weightless-waves-fragrance-free'
    # 'products_complete-curl-care-for-ultra-soft-luxurious-curls-fragrance-free'
    # 'products_deep-conditioner'
    # 'products_detangle-style-brush'
    # 'products_gentle-moisturizing-shampoo-fragrance-free'
    # 'products_hair-perfume'
    # 'products_hydrating-detangling-conditioner-fragrance-free'
    # 'products_love-ur-curls'
    # 'products_love-ur-curls-all-in-one-leave-in-for-moisturized-healthy-kinks-coils'
    # 'products_love-ur-curls-all-in-one-leave-in-for-super-soft-luxurious-curls'
    # 'products_love-ur-curls-complete-curl-care-for-moisturized-healthy-kinks-coils-1'
    # 'products_love-ur-curls-complete-curl-care-for-ultra-soft-luxurious-curls'
    # 'products_love-ur-curls-shampoo'
    # 'products_love-ur-curls-simple-3-step-system-bundle'
    # 'products_love-ur-curls-ultra-hydrating-detangling-conditioner'
    # 'products_lus-elixir-oil'
    # 'products_lus-flairosol-spray-bottle'
    # 'products_satin-scarf'
    # ]

current_path = main_path + subpath[-1]
sub_folder_path = current_path + '//screenshots2pdf//'

current_folder = os.walk(current_path)
for path, dir, filelist in current_folder:
    folder = os.path.exists(sub_folder_path)
    if not folder:
        os.makedirs(sub_folder_path)
    for filename in filelist:
        if filename.endswith('.png'):
            save_name = sub_folder_path + "%04d" % int(str(filename).rstrip('.png')) + '.jpg'
            with open(path +'/' + filename, 'rb') as f:
                im = Image.open(f)
                _width, _height = im.size
                ''' need to adjust each time! '''
                cropped = im.crop((0, 1780, 800, _height-1070))  # (left, upper, right, lower)
                new_i = cropped.convert('RGB')
                new_i.save(save_name, 'JPEG', optimize = True, quality = 90)
                f.close()

img_lst = os.listdir(sub_folder_path)
img_lst = [os.path.join(sub_folder_path, i) for i in img_lst]
pdf = FPDF('P', 'in', 'Letter') # initialize pdf layout
pdf.set_auto_page_break(0)
for image in img_lst:
    # convert pixel in inch with 1px=0.0104166667 in
    fp = open(image, 'rb')
    cover = Image.open(fp)
    width, height = cover.size
    width, height = float(width * 0.0104166667), float(height * 0.0104166667)
    fp.close()
    pdf_size = {'P': {'w': 8.5, 'h': 11}, 'L': {'w': 11, 'h': 8.5}}
    # choose portrait or landscape base on the picture shape
    if width/height >= 11/8.5:
        orientation = 'L'
        #  make sure image size is not greater than the pdf format size
        width_print = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
        pdf.add_page(orientation=orientation)
        pdf.image(image,
                  x=0.5*(11-width_print),
                  y=0.5*(8.5-height*min(height, pdf_size[orientation]['h'])/max(height, pdf_size[orientation]['h'])), 
                  w=width_print) # img resize based on page width
    elif width/height <= 8.5/11:
        orientation = 'P'
        height_print = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']
        pdf.add_page(orientation=orientation)
        pdf.image(image, 
                  x=0.5*(8.5-width*min(height, pdf_size[orientation]['h'])/max(height, pdf_size[orientation]['h'])), 
                  y=0.5*(11-height_print),
                  h=height_print) # img resize based on page height    
    else: # 8.5/11 < width/height < 11/8.5
        if width > height:
            orientation = 'L'
            height_print = height if height < pdf_size[orientation]['h'] else pdf_size[orientation]['h']
            pdf.add_page(orientation=orientation)
            pdf.image(image, 
                      x=0.5*(11-width*min(height, pdf_size[orientation]['h'])/max(height, pdf_size[orientation]['h'])), 
                      y=0.5*(8.5-height_print),
                      h=height_print) # img resize based on page height 
        else:
            orientation = 'P'
            width_print = width if width < pdf_size[orientation]['w'] else pdf_size[orientation]['w']
            pdf.add_page(orientation=orientation)
            pdf.image(image,
                      x=0.5*(8.5-width_print),
                      y=0.5*(11-height*min(height, pdf_size[orientation]['h'])/max(height, pdf_size[orientation]['h'])), 
                      w=width_print)
pdf.output(sub_folder_path + 'reviews.pdf', 'F')

fileName = 'Lusbrands_Facebook_Posts.pdf'
folderPath = screenshot_jpg
def images_crop_to_pdf(fileName, folderPath):  
    files = os.listdir(folderPath)
    files.sort(reverse = True) # key = lambda x:int(x.partition('.')[0])
    
    imgFiles = [] # pngFiles is the list with all image filenames
    for file in files:
        if file.endswith('.jpg'):
            imgFiles.append(folderPath +file)
    
    pdf = FPDF('P', 'in', 'Letter') # initialize pdf layout
    pdf.set_auto_page_break(0) # avoid blank page in between the image pages
    
    for image in imgFiles:
        # convert pixel in inch with 1px=0.0104166667 in
        fp = open(image, 'rb')
        img = Image.open(fp)
        width, height = img.size
        width_in, height_in = float(width * 0.0104166667), float(height * 0.0104166667)
        num = int(height/950)+1
        
        # set letter size 
        # pdf_size = {'P': {'w': 8.5, 'h': 11}, 'L': {'w': 11, 'h': 8.5}}
        pdf_size = {'w': 8.5, 'h': 11}
        
        if height_in <= 10:
            pdf.add_page()
            pdf.image(image,
                      x = 0.5 * (8.5 - width_in),
                      y = 0.5, #0.5*(11-height*min(height, pdf_size['h'])/max(height, pdf_size['h'])), 
                      h = height_in)
        else:
            i = 0
            while i < num:
                if i < num - 1:
                    box = (0, 950*i, 650, 950*i+950)
                    h1 = 950
                else:
                    box = (0, 950*i, 650, height)
                    h1 = height%950
                img_c = img.crop(box)
                pdf.add_page()
                pdf.image(img_c,
                          x = 0.5 * (8.5 - width_in),
                          y = 0.5, #0.5*(11-height*min(height, pdf_size['h'])/max(height, pdf_size['h'])), 
                          h = h1*0.0104166667)
                i += 1
        fp.close()
    pdf.output(folderPath + fileName + '.pdf', 'F')

# for root, dirs, files, in os.walk('E://DEI//Crawler_Code//test_dir//lusbrands.com//reviews//collections_accessories_products_lus-flairosol-spray-bottle//'):
#     for name in files:
#         if name.endswith('.png'):
#             print('delete ' + str(name))
#             os.remove(os.path.join(root, name))
         