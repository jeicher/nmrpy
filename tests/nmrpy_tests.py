import unittest
from nmrpy.data_objects import *
import numpy

class TestBaseInitialisation(unittest.TestCase):

    def test_init(self):
        base = Base()

class TestFidInitialisation(unittest.TestCase):
    
    def setUp(self):
        self.fid_good_data = [[],
                            [1, 2.0, 3.0+1j],
                            numpy.array([1, 2.0, 3.0+1j])
                            ]
        self.fid_bad_data = [
                        'string',
                        1,
                        [1, [2]],
                        [1, 2.0, 'string'],
                        [1, 2.0, Fid()],
                        ]

    def test_str(self):
        fid = Fid()
        self.assertIsInstance(fid.__str__(), str)

    def test_is_iter(self):
        for data in self.fid_good_data:
            self.assertTrue(Fid._is_iter(data))
        self.assertFalse(Fid._is_iter(1))

    def test_fid_assignment(self):
        fid = Fid()
        self.assertEqual(fid.id, None)
        self.assertIsInstance(fid.data, numpy.ndarray)
        self.assertFalse(any(self._is_iter(i) for i in fid.data))
        fid = Fid(id='string', data=self.fid_good_data[0])
        self.assertIsInstance(fid.id, str)
        self.assertIsInstance(fid.data, numpy.ndarray)
        self.assertFalse(any(self._is_iter(i) for i in fid.data))

    def test_failed_fid_assignment(self):
        for test_id in [1, []]:
            with self.assertRaises(AttributeError):
               Fid(id=test_id)
        for test_data in self.fid_bad_data:
            with self.assertRaises(AttributeError):
               Fid(data=test_data)

    def test_failed_fid_procpar_setter(self):
        fid = Fid()
        with self.assertRaises(AttributeError):
            fid._procpar = 'string'

    def test_fid_peaks_setter(self):
        fid = Fid()
        fid.peaks = numpy.array([1, 2])
        fid.peaks = [1, 2]
        self.assertIsInstance(fid.peaks, numpy.ndarray) 

    def test_failed_fid_peaks_setter(self):
        fid = Fid()
        with self.assertRaises(AttributeError):
            fid.peaks = [1, 'string']
        with self.assertRaises(AttributeError):
            fid.peaks = 'string'
        with self.assertRaises(AttributeError):
            fid.peaks = [[1,2], [3,4]]
    
    def test_fid_ranges_setter(self):
        fid = Fid()
        fid.peaks = [50, 60, 150, 160, 300]
        fid.ranges = [[1, 100], [100, 200]]
        self.assertEquals(fid._grouped_peaklist, [[50, 60],[150, 160]])

    def test_failed_fid_ranges_setter(self):
        fid = Fid()
        with self.assertRaises(AttributeError):
            fid.ranges = [1, 1]
        with self.assertRaises(AttributeError):
            fid.ranges = ['string', 1]
        with self.assertRaises(AttributeError):
            fid.ranges = [1, 1, 1]

    def test_fid_data_setter(self):
        fid = Fid()
        for data in self.fid_good_data:
            fid.data = data
            self.assertIsInstance(fid.data, numpy.ndarray)

    def test_failed_fid_data_setter(self):
        for test_data in self.fid_bad_data:
            with self.assertRaises(AttributeError):
               Fid.from_data(test_data)

    def test_real(self):
        fid = Fid.from_data(numpy.arange(10, dtype='complex'))
        fid.real()
        self.assertFalse(any(numpy.iscomplex(fid.data)))

    def test_fid_from_data(self):
        for data in self.fid_good_data:
            fid = Fid.from_data(data)
            self.assertIsInstance(fid.data, numpy.ndarray)
            self.assertEqual(list(fid.data), list(data))
        
    def test_fid_from_data_failed(self):
        for test_data in self.fid_bad_data:
            with self.assertRaises(AttributeError):
               Fid.from_data(test_data)

    def test_ps(self):
        path = './tests/test_data/test1.fid'
        fid_array = FidArray.from_path(fid_path=path, file_format='varian')
        fid = fid_array.fid00
        fid.ps(p0=20, p1=20)

    def test_ps_failed(self):
        path = './tests/test_data/test1.fid'
        fid_array = FidArray.from_path(fid_path=path, file_format='varian')
        fid = fid_array.fid00
        with self.assertRaises(AttributeError):
            fid.ps(p0='string', p1=20)
        with self.assertRaises(AttributeError):
            fid.ps(p0=34.0, p1='string')
        with self.assertRaises(AttributeError):
            fid.ps(p0=34.0, p1=4j)

    def test__is_iter_of_iters(self):
        Fid._is_iter_of_iters([[]])

    def test_failed__is_iter_of_iters(self):
        for i in [
                [],
                [1, 3],
                [1, [2]],
                ]:
            self.assertFalse(Fid._is_iter_of_iters(i))

    @staticmethod
    def _is_iter(i):
        try:
            iter(i)
            return True
        except TypeError:
            return False

    @staticmethod
    def _is_iter_of_iters(i):
        if self._is_iter(i) and all(self._is_iter(j) for j in i):
            return True
        else:
            return False

    def test_f_pk(self):
        fid = Fid()
        fid._f_pk([i for i in range(100)])
        fid._f_pk(numpy.arange(100))
        fid._f_pk(numpy.arange(100), frac_lor_gau = 2.0)
        fid._f_pk(numpy.arange(100), frac_lor_gau = -2.0)

    def test_f_pk_failed(self):
        fid = Fid()
        with self.assertRaises(ValueError):
            fid._f_pk(numpy.arange(100), offset='g')
        with self.assertRaises(ValueError):
            fid._f_pk(5)
         
    def test_f_pks(self):
        fid = Fid()
        x = numpy.arange(100)
        p1 = [10.0, 1.0, 1.0, 1.0, 1.0, 0.5]
        p2 = [20.0, 1.0, 1.0, 1.0, 1.0, 0.5]
        fid._f_pks([p1, p2], x)
        fid._f_pks([p1, p2], list(x))

    def test_f_pks_failed(self):
        fid = Fid()
        x = numpy.arange(100)
        p1 = ['j', 1.0, 1.0, 1.0, 1.0, 0.5]
        p2 = [20.0, 1.0, 1.0, 1.0, 1.0, 0.5]
        with self.assertRaises(ValueError):
            fid._f_pks([p1, p2], x)
        with self.assertRaises(ValueError):
            fid._f_pks([p2, p2], 4)
        with self.assertRaises(ValueError):
            fid._f_pks(1, 4)
        with self.assertRaises(ValueError):
            fid._f_pks([1,2], 4)

    def test_f_res(self):
        fid = Fid()
        x = numpy.arange(100)
        p1 = [10.0, 1.0, 1.0, 1.0, 1.0, 0.5]
        p2 = [20.0, 1.0, 1.0, 1.0, 1.0, 0.5]
        fid._f_res(p1+p2, x, 0.5)
        fid._f_res(p1, x, 0.5)
        fid._f_res(p1, list(x), 0.5)

    def test_f_res_failed(self):
        fid = Fid()
        x = numpy.arange(100)
        p1 = ['j', 1.0, 1.0, 1.0, 1.0, 0.5]
        p2 = [20.0, 1.0, 1.0, 1.0, 1.0, 0.5]
        with self.assertRaises(ValueError):
            fid._f_res(p1+p2, x, 0.5)
        with self.assertRaises(ValueError):
            fid._f_res(p2, 3, 0.5)
        with self.assertRaises(ValueError):
            fid._f_res('sdf', x, 0.5)
        with self.assertRaises(ValueError):
            fid._f_res(4, x, 0.5)
        with self.assertRaises(ValueError):
            fid._f_res(p2, numpy.array([x,x]), 0.5)

    def test_f_makep(self):
        fid = Fid()
        x = numpy.arange(100)
        peaks = [10, 20, 30]
        fid._f_makep(x, peaks)
        fid._f_makep(list(x), peaks)

    def test_f_makep_failed(self):
        fid = Fid()
        x = numpy.arange(100)
        peaks = [10, 20, 30]
        with self.assertRaises(ValueError):
            fid._f_makep(x, 1)
        with self.assertRaises(ValueError):
            fid._f_makep(1, peaks)
        with self.assertRaises(ValueError):
            fid._f_makep(numpy.array([x,x]), peaks)
        with self.assertRaises(ValueError):
            fid._f_makep(x, 2*[peaks])

    def test_f_conv(self):
        fid = Fid()
        x = 1+numpy.arange(100)
        data = 1/x**2
        p1 = [10.0, 1.0, 1.0, 1.0, 1.0, 0.5]
        p2 = [20.0, 1.0, 1.0, 1.0, 1.0, 0.5]
        fid._f_conv([p1, p2], data)
        fid._f_conv([p1, p2], list(data))

    def test_f_conv_failed(self):
        fid = Fid()
        x = 1+numpy.arange(100)
        data = 1/x**2
        p1 = [10.0, 1.0, 1.0, 1.0, 1.0, 0.5]
        p2 = [20.0, 1.0, 1.0, 1.0, 1.0, 0.5]
        with self.assertRaises(ValueError):
            fid._f_conv([p1, p2], 1)
        with self.assertRaises(ValueError):
            fid._f_conv(1, data)
        with self.assertRaises(ValueError):
            fid._f_conv([p1, p2], numpy.array(2*[data]))

    def test_f_fitp(self):
        path = './tests/test_data/test1.fid'
        fid_array = FidArray.from_path(fid_path=path, file_format='varian')
        peaks = [100,200]
        data_index = [0,2000]
        fid = fid_array.get_fids()[0]
        fid.peaks = peaks
        fid._f_fitp(data_index, fid.peaks, 0.5)
        fid.data = list(fid.data)
        fid._f_fitp(data_index, peaks, 0.5)

    def test_f_fitp_failed(self):
        path = './tests/test_data/test1.fid'
        fid_array = FidArray.from_path(fid_path=path, file_format='varian')
        peaks = [100,200]
        data_index = [0,2000]
        fid = fid_array.get_fids()[0]
        with self.assertRaises(ValueError):
            fid._f_fitp(1, peaks, 0.5)
        with self.assertRaises(ValueError):
            fid._f_fitp([1, 1], peaks, 0.5)
        with self.assertRaises(ValueError):
            fid._f_fitp([1], peaks, 0.5)

class TestFidArrayInitialisation(unittest.TestCase):
    
    def setUp(self):
        self.fid_data = [1, 2.0, 3.0+1j]
        self.fid = Fid(id='fid0', data=self.fid_data)
        self.fids = [Fid(id='fid%i'%id, data=self.fid_data) for id in range(10)]

    def test_fid_array_assignment(self):
        fid_array = FidArray()
        self.assertTrue(fid_array.id is None)
        fid_array = FidArray(id='string')
        self.assertTrue(fid_array.id is 'string')
        print(fid_array)

    def test_failed_fid_array_assignment(self):
        with self.assertRaises(AttributeError):
            FidArray(id=1)
    
    def test_failed_fid_array_from_dataable(self):
        fid_data_array = [1, 2.0, 3.0+1j] 
        with self.assertRaises(AttributeError):
            FidArray.from_data(fid_data_array)

    def test_fid_array_add_fid(self):
        fid_array = FidArray()
        fid_array.add_fid(self.fid)
        self.assertEqual(fid_array.get_fid(self.fid.id), self.fid)

    def test_fid_array_add_fid_failed(self):
        fid_array = FidArray()
        with self.assertRaises(AttributeError):
            fid_array.add_fid('not and fid')

    def test_failed_fid_array_add_fid(self):
        fid_array = FidArray()
        with self.assertRaises(AttributeError):
            fid_array.add_fid('not_fid')

    def test_failed_fid_array_procpar_setter(self):
        fid_array = FidArray()
        with self.assertRaises(AttributeError):
            fid_array._procpar = 'string'

    def test_failed_fid_array_data_setter(self):
        fid_array = FidArray()
        with self.assertRaises(AttributeError):
            fid_array.data = 'string'

    def test_fid_array_del_fid(self):
        fid_array = FidArray()
        fid_array.add_fid(self.fid)
        fid_array.del_fid(self.fid.id)

    def test_failed_fid_array_del_fid(self):
        fid_array = FidArray()
        fid_array.add_fid(self.fid)
        with self.assertRaises(AttributeError):
            fid_array.del_fid('non_existent_fid')
        fid_array.string = 'string'
        with self.assertRaises(AttributeError):
            fid_array.del_fid('string')

    def test_failed_fid_array_get_fid(self):
        fid_array = FidArray()
        self.assertEqual(fid_array.get_fid('non_existent_fid'), None)

    def test_failed_fid_array_add_fid(self):
        fid_array = FidArray()
        with self.assertRaises(AttributeError):
            fid_array.add_fid(1)

    def test_fid_array_add_fid(self):
        fid_array = FidArray()
        fid_array.add_fids(self.fids)

    def test_failed_fid_array_add_fid(self):
        fid_array = FidArray()
        fid_array.add_fids(self.fids+['string'])

    def test_from_data(self):
        data_array = 3*[self.fid_data] 
        fid_array = FidArray.from_data(data_array)
        self.assertIsInstance(fid_array, FidArray)
        for fid_id in ['fid%i'%i for i in range(len(data_array))]:
            fid = fid_array.get_fid(fid_id)
            self.assertIsInstance(fid, Fid)

    def test_from_path_single(self):
        path = './tests/test_data/test2.fid'
        fid_array = FidArray.from_path(fid_path=path)
        self.assertIsInstance(fid_array._procpar, dict)
        self.assertIsInstance(fid_array._params, dict)

    def test_fid_params_setter_failed(self):
        fid = Fid()
        with self.assertRaises(AttributeError):
            fid._params = 'not a dictionary'
 
    def test_from_path_array(self):
        path = './tests/test_data/test1.fid'
        fid_array = FidArray.from_path(fid_path=path)
        self.assertIsInstance(fid_array._procpar, dict)
        self.assertIsInstance(fid_array._params, dict)
        path = './tests/test_data/bruker1'
        fid_array = FidArray.from_path(fid_path=path)
        self.assertIsInstance(fid_array._procpar, dict)
        self.assertIsInstance(fid_array._params, dict)

    def test_from_path_array_varian(self):
        path = './tests/test_data/test1.fid'
        fid_array = FidArray.from_path(fid_path=path, file_format='varian')
        self.assertIsInstance(fid_array._procpar, dict)
        self.assertIsInstance(fid_array._params, dict)

    def test_from_path_array_bruker(self):
        path = './tests/test_data/bruker1'
        fid_array = FidArray.from_path(fid_path=path, file_format='bruker')
        self.assertIsInstance(fid_array._procpar, dict)
        self.assertIsInstance(fid_array._params, dict)

    def test_failed_from_path_array_varian(self):
        path = './tests/test_data/bruker1'
        with self.assertRaises(AttributeError):
            fid_array = FidArray.from_path(fid_path=path, file_format='varian')
        path = './tests/test_data/non_existent'
        with self.assertRaises(FileNotFoundError):
            fid_array = FidArray.from_path(fid_path=path, file_format='varian')

    def test_failed_from_path_array_bruker(self):
        path = './tests/test_data/test1.fid'
        with self.assertRaises(AttributeError):
            fid_array = FidArray.from_path(fid_path=path, file_format='bruker')
        path = './tests/test_data/non_existent'
        with self.assertRaises(FileNotFoundError):
            fid_array = FidArray.from_path(fid_path=path, file_format='bruker')

    def test_array_procpar(self):
        path = './tests/test_data/test2.fid'
        fid_array = FidArray.from_path(path)
        self.assertIsInstance(fid_array._procpar, dict)
        self.assertIsInstance(fid_array._params, dict)

    def test_data_property(self):
        path = './tests/test_data/test1.fid'
        fid_array = FidArray.from_path(path)
        self.assertIsInstance(fid_array.data, numpy.ndarray)

    def test_failed_from_path_array(self):
        path = None
        with self.assertRaises(AttributeError):
            fid_array = FidArray.from_path(path)
        path = 'non_existent_path'
        with self.assertRaises(OSError):
            fid_array = FidArray.from_path(path)

    def test_failed_from_path_array_varian(self):
        path = None
        with self.assertRaises(AttributeError):
            fid_array = FidArray.from_path(path, file_format='varian')
        path = 'non_existent_path'
        with self.assertRaises(OSError):
            fid_array = FidArray.from_path(path, file_format='varian')

    def test_failed_from_path_array_bruker(self):
        path = None
        with self.assertRaises(AttributeError):
            fid_array = FidArray.from_path(path, file_format='bruker')
        path = 'non_existent_path'
        with self.assertRaises(OSError):
            fid_array = FidArray.from_path(path, file_format='bruker')

    def test__is_iter_of_iters(self):
        FidArray._is_iter_of_iters([[]])

    def test_failed__is_iter_of_iters(self):
        for i in [
                [],
                [1, 3],
                [1, [2]],
                ]:
            self.assertFalse(FidArray._is_iter_of_iters(i))

    @staticmethod
    def _is_iter(i):
        try:
            iter(i)
            return True
        except TypeError:
            return False

    @staticmethod
    def _is_iter_of_iters(i):
        if self._is_iter(i) and all(self._is_iter(j) for j in i):
            return True
        else:
            return False

if __name__ == '__main__':
    unittest.main()
