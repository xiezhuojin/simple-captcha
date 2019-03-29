import random
import string
import os

from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageFilter


class Captcha:
	"""A simple captcha generator returns a PIL captcha object and it's answer.

	"""
	UPPER_CASE = string.ascii_uppercase
	LOWER_CASE = string.ascii_lowercase
	NUMBER = '0123456789'

	@classmethod
	def random_string(cls, length: int, char_set):
		if length <= 0:
			raise ValueError('length should be at least 1')
		random_str = ''
		for i in range(length):
			random_str += random.choice(char_set)
		return random_str

	@classmethod
	def random_color(cls):
		return tuple(random.randint(0, 255) for i in range(3))

	def __init__(
		self, size: tuple, char_length=5, lines: int=3, draw_dots: float=0.3, 
		twist=True, random_bg_color=True
		):
		if lines < 0:
			raise ValueError('lines should at least 0')
		self.size = size
		self.char_length = char_length
		self.lines = lines
		self.draw_dots = draw_dots
		self.twist = twist
		self.random_bg_color = random_bg_color

	def _create_image(self):
		image =	Image.new(
			'RGB', self.size, 
			self.random_color() if self.random_bg_color==True else (255, 255, 255))
		return image

	def _draw_chars(self, image, chars):
		image_length, image_width = image.size
		# calculate font size
		font_size = 0
		font = ImageFont.truetype('/Library/Fonts/Arial.ttf', size=font_size)
		while font.getsize(chars)[0] < image_length * 0.7:
			font_size += 1
			font = ImageFont.truetype('/Library/Fonts/Arial.ttf', size=font_size)
		# calculate start coordinate
		x = (image.size[0] - font.getsize(chars)[0]) / 2
		y = (image.size[1] - font.getsize(chars)[1]) / 2
		x_gap = font.getsize(chars[0])[0]
		# draw line
		for i in range(self.char_length):
			# create a template
			d = ImageDraw.Draw(image)
			d.text(
				(x + i*x_gap + random.uniform(-x*0.1, x*0.1), y + random.uniform(-y*0.3, y*0.3)), 
				chars[i], 
				fill=self.random_color(), 
				font=ImageFont.truetype('/Library/Fonts/Arial.ttf', size=font_size)
			)
		return image
		
	def _draw_lines(self, image):
		image_length, image_width = image.size
		d = ImageDraw.Draw(image)
		for i in range(self.lines):
			d.line(
				[
					(random.randint(0, image_length), random.randint(0, image_width)), 
					(random.randint(0, image_length), random.randint(0, image_width))
				],
				fill=self.random_color(),
				width=random.randint(1, 3)
			)
			d.arc(
				[
					(random.randint(0, image_length), random.randint(0, image_width)), 
					(random.randint(0, image_length), random.randint(0, image_width))
				],
				start = random.randint(0, 360),
				end = random.randint(0, 360),
				width=random.randint(1, 3)
			)
		return image

	def _draw_dots(self, image):
		image_length, image_width = image.size
		d = ImageDraw.Draw(image)
		if self.draw_dots > 0:
			for x in range(image_length):
				for y in range(image_width):
					if random.randint(0, 100) < self.draw_dots*10:
						d.point((x, y), fill=self.random_color())
		return image

	def _twist_image(self, image):
		if self.twist == True:
			params = [
				1 - float(random.randint(1, 2)) / 1000,
       			0,
       			0,
       			0,
       			1 - float(random.randint(1, 10)) / 1000,
       			float(random.randint(1, 2)) / 2000,
       			0.001,
       			float(random.randint(1, 2)) / 3000
       		]
			image = image.transform(image.size, Image.PERSPECTIVE, params)
			image.filter(ImageFilter.EDGE_ENHANCE_MORE)
		return image

	def get_captcha(self):
		image = self._create_image()
		chars = self.random_string(self.char_length, self.UPPER_CASE+self.LOWER_CASE)
		image = self._draw_chars(image, chars)
		image = self._draw_lines(image)
		image = self._draw_dots(image)
		image = self._twist_image(image)
		return image, chars

if __name__ == '__main__':
	c = Captcha((200, 150))
	import time
	start = time.time()
	for i in range(4):
		captcha, _ = c.get_captcha()
		# captcha.save()
		captcha.save(f'/Users/xiezhuojin/Documents/python/captcha.py/example/{i}.jpg')
	print(f'toke {time.time()-start}s')