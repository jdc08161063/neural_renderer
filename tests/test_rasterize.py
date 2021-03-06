import unittest

import chainer
import chainer.gradient_check
import chainer.testing
import cupy as cp
import scipy.misc

import neural_renderer


class TestRasterize(unittest.TestCase):
    def test_case1(self):
        # load teapot
        vertices, faces = neural_renderer.load_obj('./tests/data/teapot.obj')
        vertices = vertices[None, :, :]
        faces = faces[None, :, :]
        vertices = chainer.cuda.to_gpu(vertices)
        faces = chainer.cuda.to_gpu(faces)
        textures = cp.ones((1, faces.shape[1], 4, 4, 4, 3), 'float32')

        # create renderer
        renderer = neural_renderer.Renderer()
        renderer.image_size = 256
        renderer.anti_aliasing = False

        images = renderer.render(vertices, faces, textures)
        images = images.data.get()
        image = images[0]
        image = image.transpose((1, 2, 0))

        scipy.misc.imsave('./tests/data/test_rasterize1.png', image)

    def test_case2(self):
        # load teapot
        vertices, faces = neural_renderer.load_obj('./tests/data/teapot.obj')
        vertices = vertices[None, :, :]
        faces = faces[None, :, :]
        vertices = chainer.cuda.to_gpu(vertices)
        faces = chainer.cuda.to_gpu(faces)
        textures = cp.ones((1, faces.shape[1], 4, 4, 4, 3), 'float32')

        # create renderer
        renderer = neural_renderer.Renderer()
        renderer.eye = [1, 1, -2.7]

        images = renderer.render(vertices, faces, textures)
        images = images.data.get()
        image = images[0]
        image = image.transpose((1, 2, 0))

        scipy.misc.imsave('./tests/data/test_rasterize2.png', image)


if __name__ == '__main__':
    unittest.main()
