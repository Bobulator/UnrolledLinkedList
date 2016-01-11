import unittest
from unrolled_linked_list import UnrolledLinkedList

__author__ = 'Chad Bacon'
__email__ = 'chadsbacon@gmail.com'

'''
> Implement your tests here

To run your tests, just run `python tests.py`
'''


class ExampleTest(unittest.TestCase):
    """ Demonstrates how the unittest framework works """

    def test_default_constructor(self):
        new_list = UnrolledLinkedList()
        self.assertIsNotNone(new_list)
        self.assertEqual(16, new_list.max_node_capacity)
        self.assertEqual(0, len(new_list))

    def test_constructor(self):
        new_list = UnrolledLinkedList(20)
        self.assertIsNotNone(new_list)
        self.assertEqual(20, new_list.max_node_capacity)
        self.assertEqual(0, len(new_list))

        new_list = UnrolledLinkedList(1)
        self.assertIsNotNone(new_list)
        self.assertEqual(1, new_list.max_node_capacity)
        self.assertEqual(0, len(new_list))

        self.failUnlessRaises(AssertionError, UnrolledLinkedList, 0)
        self.failUnlessRaises(AssertionError, UnrolledLinkedList, -1)

    def test_append(self):
        l = UnrolledLinkedList(4)
        l.append(1)
        self.assertEqual(1, len(l))
        self.assertEqual([1], l.head.data_list)

        l.append(2)
        self.assertEqual(2, len(l), )
        self.assertEqual([1, 2], l.head.data_list)

        l.append(3)
        l.append(4)
        self.assertEqual(4, len(l))
        self.assertEqual([1, 2, 3, 4], l.head.data_list)

        l = UnrolledLinkedList(5)
        for i in range(11):
            l.append(i)
        self.assertEqual('{[0, 1, 2], [3, 4, 5], [6, 7, 8, 9, 10]}', str(l))

    def test_split(self):
        l = UnrolledLinkedList(4)
        for i in range(1, 6):
            l.append(i)
        self.assertEqual(5, len(l))
        self.assertNotEqual(l.head, l.tail)
        self.assertEqual([1, 2], l.head.data_list)
        self.assertEqual([3, 4, 5], l.tail.data_list)

        l.append(6)
        l.append(7)
        self.assertEqual(7, len(l))
        self.assertNotEqual(l.head.next_node, l.tail)
        self.assertEqual([3, 4], l.head.next_node.data_list)
        self.assertEqual([5, 6, 7], l.tail.data_list)

    def test_str(self):
        l = UnrolledLinkedList(4)
        self.assertEqual('{}', str(l))

        for i in range(1, 8):
            l.append(i)

        self.assertEqual('{[1, 2], [3, 4], [5, 6, 7]}', str(l))

    def test_add(self):
        list1 = UnrolledLinkedList(4)
        list2 = ['not', 'an', 'UnrolledLinkedList']
        self.assertRaises(TypeError, list1.__add__, list2)

        list2 = UnrolledLinkedList(4)

        test_list = list1 + list2
        self.assertEqual(0, len(test_list))

        st = 'abcde'
        for c in st:
            list2.append(c)

        list1 += list2
        self.assertEqual(5, len(list1))

        list2 = UnrolledLinkedList()
        list2 = list1 + list2
        self.assertEqual(5, len(list2))

        list1 = UnrolledLinkedList(4)
        for i in range(5):
            list1.append(i)
        list2 = UnrolledLinkedList(10)
        for i in range(5, 21):
            list2.append(i)

        test_list = list1 + list2

        self.assertEqual(len(list1) + len(list2), len(test_list))
        self.assertEqual([18, 19, 20], test_list.tail.data_list)

    def test_contains(self):
        l = UnrolledLinkedList(5)

        self.assertFalse(0 in l)

        l.append(0)
        self.assertTrue(0 in l)

        for i in range(5):
            l.append(i)

        self.assertTrue(4 in l)
        self.assertTrue(3 in l)
        self.assertTrue(2 in l)
        self.assertTrue(1 in l)

        self.assertFalse(5 in l)
        self.assertFalse(-1 in l)

    def test_getitem(self):
        l = UnrolledLinkedList(3)
        for i in range(9):
            l.append(i)

        self.assertRaises(TypeError, l.__getitem__, '0')
        self.assertRaises(IndexError, l.__getitem__, 9)
        self.assertRaises(IndexError, l.__getitem__, -10)
        
        for i in range(9):
            self.assertEqual(i, l[i])
        self.assertEqual(8, l[-1])
        self.assertEqual(5, l[-4])

    def test_getitem_slice(self):
        l = UnrolledLinkedList(5)
        for x in range(20):
            l.append(x)

        new_list = l[5:10]
        self.assertEqual(5, len(new_list))
        self.assertEqual(20, len(l))
        self.assertEqual('{[5, 6, 7, 8, 9]}', str(new_list))

        new_list = l[:]
        self.assertEqual(len(l), len(new_list))
        self.assertEqual(str(l), str(new_list))

        new_list = l[::2]
        self.assertEqual(10, len(new_list))
        for i in range(10):
            self.assertEqual(i*2, new_list[i])

        new_list = l[1::2]
        self.assertEqual(10, len(new_list))
        for i in range(0, 10):
            self.assertEqual((i*2)+1, new_list[i])

    def test_setitem(self):
        l = UnrolledLinkedList(5)
        for i in range(11):
            l.append(i)

        self.assertRaises(TypeError, l.__setitem__, '0', 99)
        self.assertRaises(IndexError, l.__setitem__, 11, 99)
        self.assertRaises(IndexError, l.__setitem__, -12, 99)

        l[0] = 100
        self.assertEqual(100, l[0])
        l[1] = 101
        self.assertEqual(101, l[1])
        l[2] = 102
        self.assertEqual(102, l[2])
        l[4] = 104
        self.assertEqual(104, l[4])
        l[5] = 105
        self.assertEqual(105, l[5])
        self.assertEqual(105, l[-6])
        l[-5] = 106
        self.assertEqual(106, l[-5])
        l[-4] = 107
        self.assertEqual(107, l[-4])
        l[-2] = 109
        self.assertEqual(109, l[-2])
        l[-1] = 110
        self.assertEqual(110, l[-1])

        self.assertEqual('{[100, 101, 102], [3, 104, 105], [106, 107, 8, 109, 110]}', str(l))

    def test_setitem_slice(self):
        l = UnrolledLinkedList(10)
        for i in range(5):
            l.append(i)

        t = UnrolledLinkedList(2)
        for i in range(10):
            t.append(9)

        l[2:3] = t

        self.assertEqual(14, len(l))
        self.assertEqual(1, l[1])
        for i in range(2, 12):
            self.assertEqual(9, l[i])
        self.assertEqual(3, l[12])

        t = UnrolledLinkedList(2)
        t.append(2)

        l[2:12] = t
        self.assertEqual(5, len(l))
        self.assertEqual('{[0, 1, 2, 3, 4]}', str(l))

        l[:] = t
        self.assertEqual(1, len(l))
        self.assertEqual('{[2]}', str(l))

        l = UnrolledLinkedList(5)
        test_list = [1, 2, 6, 9, 6, 1, 0, 8, 1, 8, 2, 6]
        for x in test_list:
            l.append(x)

        t = UnrolledLinkedList(3)
        test_list2 = [3, 6, 8, 4]
        for x in test_list2:
            t.append(x)

        l[0:2] = t
        self.assertEqual(14, len(l))

    def test_mul(self):
        l = UnrolledLinkedList(6)
        l.append(1)
        l.append(2)

        self.assertRaises(TypeError, l.__mul__, '4')

        l *= 1
        self.assertEqual(2, len(l))
        self.assertEqual(6, l.max_node_capacity)
        self.assertEqual('{[1, 2]}', str(l))

        list2 = l * 4
        self.assertEqual(8, len(list2))
        self.assertEqual(6, list2.max_node_capacity)
        self.assertEqual('{[1, 2, 1], [2, 1, 2, 1, 2]}', str(list2))

        l *= 0
        self.assertEqual(0, len(l))
        self.assertEqual(6, l.max_node_capacity)

        l = UnrolledLinkedList()

        l *= 10
        self.assertEqual(0, len(l))

    def test_delitem(self):
        l = UnrolledLinkedList(4)
        l.append('a')

        self.assertRaises(TypeError, l.__delitem__, '0')
        self.assertRaises(IndexError, l.__delitem__, 1)
        self.assertRaises(IndexError, l.__delitem__, -2)

        del l[0]
        self.assertEqual(0, len(l))
        self.assertIsNone(l.head)
        self.assertIsNone(l.tail)
        self.assertRaises(IndexError, l.__delitem__, 0)

        l.append('a')
        l.append(0)

        del l[0]
        self.assertEqual(1, len(l))
        self.assertEqual(0, l[0])

        del l[0]
        self.assertEqual(0, len(l))
        self.assertIsNone(l.head)
        self.assertIsNone(l.tail)

        l.append('a')
        l.append(0)
        l.append(1)
        l.append(2)
        l.append(3)
        l.append(4)

        del l[0]
        self.assertEqual(5, len(l))
        self.assertEqual([0, 1], l.head.data_list)
        self.assertEqual([2, 3, 4], l.tail.data_list)
        self.assertEqual('{[0, 1], [2, 3, 4]}', str(l))

        del l[-1]
        self.assertEqual(4, len(l))
        self.assertEqual('{[0, 1], [2, 3]}', str(l))

        del l[1]
        self.assertEqual(3, len(l))
        self.assertEqual('{[0, 2, 3]}', str(l))
        self.assertEqual(l.head, l.tail)

        del l[1]
        del l[1]

        for i in range(1, 7):
            l.append(i)

        self.assertEqual(7, len(l))

        del l[2]
        self.assertEqual(6, len(l))
        self.assertEqual([3, 4], l.head.next_node.data_list)
        self.assertEqual([5, 6], l.tail.data_list)

        del l[2]
        self.assertEqual(5, len(l))
        self.assertEqual([4, 5, 6], l.tail.data_list)
        self.assertEqual(l.head.next_node, l.tail)

        del l[4]
        self.assertRaises(IndexError, l.__delitem__, 4)

        del l[2]
        self.assertEqual(3, len(l))
        self.assertEqual(5, l[2])
        self.assertEqual('{[0, 1, 5]}', str(l))

        del l[2]
        for i in range(2, 11):
            l.append(i)

        del l[2]
        self.assertEqual('{[0, 1], [3, 4, 5], [6, 7], [8, 9, 10]}', str(l))
        del l[0]
        self.assertEqual('{[1, 3], [4, 5], [6, 7], [8, 9, 10]}', str(l))
        del l[4]
        self.assertEqual('{[1, 3], [4, 5], [7, 8], [9, 10]}', str(l))
        del l[7]
        self.assertEqual('{[1, 3], [4, 5], [7, 8, 9]}', str(l))
        del l[4]
        del l[4]
        self.assertEqual('{[1, 3], [4, 5, 9]}', str(l))

        l = UnrolledLinkedList(6)
        for i in xrange(20):
            l.append(i)
        del l[4]
        del l[-1]
        self.assertEqual(18, len(l))
        self.assertEqual(18, l[-1])
        for i in reversed(xrange(5, 18)):
            self.assertEqual(i+1, l[i])

        l = UnrolledLinkedList(3)
        for i in xrange(8):
            l.append(i)
        self.assertEqual(8, len(l))
        del l[-1]
        self.assertEqual(7, len(l))
        self.assertEqual(6, l[6])
        del l[-2]
        self.assertEqual(6, len(l))
        self.assertEqual(6, l[5])

    def test_delitem_slice(self):
        l = UnrolledLinkedList(4)
        for i in range(8):
            l.append(i)

        self.assertEqual(8, len(l))

        del l[:4]
        self.assertEqual(4, len(l))
        self.assertEqual('{[4, 5], [6, 7]}', str(l))

        del l[-50:20]
        self.assertEqual(0, len(l))
        self.assertIsNone(l.head)
        self.assertIsNone(l.tail)

        for i in range(8):
            l.append(i)

        del l[1:8]
        self.assertEqual(1, len(l))
        self.assertEqual('{[0]}', str(l))

        del l[0]
        for i in range(8):
            l.append(i)

        del l[:7]
        self.assertEqual(1, len(l))
        self.assertEqual('{[7]}', str(l))

        del l[0]
        for i in range(8):
            l.append(i)

        del l[1:7]
        self.assertEqual(2, len(l))
        self.assertEqual('{[0, 7]}', str(l))

        del l[0:]
        self.assertEqual(0, len(l))
        self.assertIsNone(l.head)
        self.assertIsNone(l.tail)

        for i in range(8):
            l.append(i)

        del l[3:7]
        self.assertEqual(4, len(l))
        self.assertEqual('{[0, 1], [2, 7]}', str(l))

        del l[2]
        self.assertEqual(3, len(l))
        self.assertEqual('{[0, 1, 7]}', str(l))

        del l[:]
        self.assertEqual(0, len(l))

        for i in range(10):
            l.append(i)

        del l[::2]
        self.assertEqual('{[1, 3], [5, 7, 9]}', str(l))

    def test_iter(self):
        l = UnrolledLinkedList()

        i = 0
        for x in l:
            i += 1
        self.assertEqual(0, i)

        for i in range(50):
            l.append(i)

        for i, x in enumerate(l):
            self.assertEqual(i, x)
            self.assertEqual(l[i], x)

        del l[40]
        del l[30]
        del l[20]
        del l[10]
        del l[0]

        i = 0
        for x in l:
            if i % 10 == 0:
                self.assertNotEqual(i, x)
                i += 1
                self.assertEqual(i, x)
            else:
                self.assertEqual(i, x)
            i += 1

    def test_reversed(self):
        l = UnrolledLinkedList()

        i = 0
        for x in reversed(l):
            i += 1
        self.assertEqual(0, i)

        for i in range(50):
            l.append(i)

        i = 1
        for x in reversed(l):
            self.assertEqual(l[-i], x)
            i += 1

    def test_general(self):
        l = UnrolledLinkedList(16)
        for i in range(1000):
            l.append(i)

        self.assertEqual(1000, len(l))
        self.assertTrue(999 in l)
        self.assertTrue(50 in l)

        for i in range(250, 750):
            l[i] = 'delete me'

        self.assertEqual(1000, len(l))
        self.assertTrue('delete me' in l)
        self.assertEqual(249, l[249])
        self.assertEqual('delete me', l[250])
        self.assertEqual('delete me', l[251])
        self.assertEqual('delete me', l[748])
        self.assertEqual('delete me', l[749])
        self.assertEqual(750, l[750])

        for i in range(500):
            del l[250]

        self.assertEqual(500, len(l))
        self.assertFalse('delete me' in l)
        self.assertTrue(750, l[250])
        self.assertTrue(499, 999)

        for i in range(10):
            del l[499 - (i * 40)]

        self.assertEqual(490, len(l))
        self.assertFalse(999 in l)

        for i in range(489):
            del l[0]

        self.assertEqual(1, len(l))
        self.assertTrue(998 in l)
        self.assertTrue(998, l[0])

if __name__ == '__main__':
    unittest.main()
