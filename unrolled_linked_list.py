from copy import deepcopy

__author__ = 'Chad Bacon'
__email__ = 'chadsbacon@gmail.com'


class UnrolledLinkedList(object):
    """ This is the container class for your unrolled linked list """

    class Node(object):
        """ This is the node object you should use within your unrolled linked
            list
        """

        def __init__(self, data_list, next_node=None):
            """
            :param data_list: Initial list to be stored
            :param next_node: Pointer to the next Node in the Linked List
            """
            self.data_list = data_list
            self.next_node = next_node

        def append(self, data):
            """Adds an item to the end of this Node's list.
            :param data: data to be added to the Node's list
            """
            self.data_list.append(data)

        def __str__(self):
            """ Converts the node's data list to a comma separated string
            :return: string
            """
            str_list = ['[']
            for i in self.data_list:
                str_list.append(str(i))
                str_list.append(', ')
            str_list.pop()  # remove trailing space
            str_list.append("]")

            return ''.join(str_list)

    def __init__(self, max_node_capacity=16):
        """  The constructor for the list.

        The default max node capacity is 16, but this value should be
        overridable.

        """
        assert isinstance(max_node_capacity, int)
        assert max_node_capacity > 0
        self.max_node_capacity = max_node_capacity
        self.length = 0
        self.head = None
        self.tail = None

    def __add__(self, other):
        """ Appends two Unrolled Linked Lists end-to-end using `+`

        Usage: `
            list_one = UnrolledLinkedList()
            list_two = UnrolledLinkedList()
            new_list = list_one + list_two
        `

        Args:
            other: Another Unrolled Linked List object. The new ULL should have
                the same max capacity as the current ULL.

        Returns:
            A new unrolled linked list.

        Raises:
            TypeError: If the passed in `other` parameter is not an unrolled
                linked list, raise this error. Users should not be able to
                append anything to an unrolled linked list besides another
                unrolled linked list.
        """
        if not isinstance(other, UnrolledLinkedList):
            raise TypeError("Can only add object of type UnrolledLinkedList")

        # Copy the current list and add the contents of other to it
        new_list1 = deepcopy(self)
        for x in other:
            new_list1.append(x)

        return new_list1

    def __mul__(self, count):
        """ Repeats (multiplies) the list a given number of times

        Usage: `my_list *= 5` should return a list of itself repeated 5x

        Args:
            count: An integer indicating the number of times the list should
                be repeated.

        Returns:
            The new data structure multiplied however many times indicated

        Raises:
            TypeError: If count is not an int

        """
        if not isinstance(count, int):
            raise TypeError("Count must be an int")

        # If nothing is in the list mul won't do anything
        if self.length == 0:
            return self

        # Assuming that a list times 0 or less should return an empty list
        if count <= 0:
            return UnrolledLinkedList(self.max_node_capacity)

        # Copy the initial list (self *= 1) then keep re-adding
        # elements as determined by count.
        new_list = deepcopy(self)
        for i in range(count - 1):
            for x in self:
                new_list.append(x)

        return new_list

    def __getitem__(self, index):
        """ Access the element at the given index.

        The indexes of an unrolled linked list refers to the total collection
        of the list. i.e. in {[1, 2, 3], [5, 4, 1]}, index @ 1 refers to the
        value 2. Index @ 4 refers to the value 4, even though it is in another
        node.

        This function should support negative indices, which are natural to
        Python. For example, getting at index -1 should return the last
        element, index -2 should be the second-to-last element and so on.

        Usage: `my_list[4]`

        BONUS: Allow this to work with slices. The resulting structure should
        be a new balanced unrolled linked list.
        For example,
        my_list = {[1, 2, 6], [9, 6, 1], [0, 8, 1], [8, 2, 6]}
        then my_list[4:10] should be {[6, 1, 0], [8, 1, 8, 2, 6]}

        Args:
            index: An int value indicating an index in the list.

        Returns:
            The object held at the given `index`.

        Raises:
            TypeError: If index is not an `int` object.
            IndexError: If the index is out of bounds.

        """
        # If input is a slice then generate a new list by adding
        # elements to it as determined by the slice attributes.
        if isinstance(index, slice):
            new_list = UnrolledLinkedList(self.max_node_capacity)
            for i in xrange(*index.indices(len(self))):
                if i > -(len(self) + 1) or i < len(self):
                    new_list.append(self[i])
            return new_list

        self.__verify_index(index)

        if index < 0:
            index += self.length

        index, prev_node, cur_node = self.__find_node_index(index)
        return cur_node.data_list[index]

    def __len__(self):
        """Return the total number of items in the list

        Usage: `len(my_list)`

        Returns:
            An int object indicating the *total* number of items in the list,
            NOT the number of nodes.
        """
        return self.length

    def __setitem__(self, index, value):
        """ Sets the item at the given index to a new value

        Usage: `my_list[5] = "my new value"`

        BONUS: Allow this to work with slices. You should *only* be able to
        assign another unrolled linked list. Upon doing so, you should
        rebalance the list. For example, if your node max capacity is 5, and
        your list is:
        my_list = {[1, 2, 6], [9, 6, 1], [0, 8, 1], [8, 2, 6]}
        and you have another list with a different max capacity:
        other_list = {[3, 6], [8, 4]},
        and you use `my_list[0:2] = other_list` the result should be
        {[3, 6, 8, 4, 6], [9, 6, 1], [0, 8, 1], [8, 2, 6]}
        which is acceptable since the max capacity is 5. Node 0 did not go over

        Args:
            index: The index of the list which should be modified.
            value: The new value for the list at the given index.

        Returns:
            none - this is a void function and should mutate the data structure
                in-place.

        Raises:
            TypeError: If index is not an `int` object.
            IndexError: If the index is out of bounds.
        """
        if isinstance(index, slice):
            del self[index]
            offset = 0
            if len(self) == 0:
                for x in value:
                    self.append(x)
            else:
                for x in xrange(*index.indices(len(self))):
                    self.__insert(x + offset, value)
                    offset += value.length
                    if not index.step:
                        break
            return

        self.__verify_index(index)

        if index < 0:
            index += self.length

        index, prev_node, cur_node = self.__find_node_index(index)
        cur_node.data_list[index] = value

    def __delitem__(self, index):
        """ Deletes an item using the built-in `del` keyword

        This function should support negative indices, which are natural to
        Python. For example, deleting at index -1 should delete the last
        element, index -2 should be the second-to-last element and so on.

        RULES FOR DELETING (paraphrased from Wikipedia):
        To remove an element, we simply find the node it is in and delete it
        from the elements array, decrementing numElements. If this reduces the
        node to less than half-full, then we move elements from the next node
        to fill it back up above half. If this leaves the next node less than
        half full, then we move all its remaining elements into the current
        node, then bypass and delete it.

        BONUS: Allow this to delete using slices as well as indices
        (http://stackoverflow.com/questions/12986410/how-to-implement-delitem-to-handle-all-possible-slice-scenarios)

        Usage: `del my_list[4]`

        Args:
            index: An `int` value indicating the index of the item you are
                deleting.

        Returns:
            none - this is a void function that should mutate the data
                structure in-place, not return a new data structure.

        Raises:
            TypeError: If index is not an `int` object.
            IndexError: If the index is out of bounds.
        """
        # If input is a slice then delete all elements as determined
        # by the slice attributes, using an offset to account for the
        # changing size of the list.
        if isinstance(index, slice):
            offset = 0
            for i in xrange(*index.indices(len(self))):
                if i > -(len(self) + 1) or i < len(self):
                    del self[i - offset]
                    offset += 1
            return

        self.__verify_index(index)

        if index < 0:
            index += self.length

        index, prev_node, cur_node = self.__find_node_index(index)
        del cur_node.data_list[index]
        self.length -= 1

        self.__balance_node(prev_node, cur_node)

    def __iter__(self):
        """ Returns an iterable to allow one to iterate the list.

        This dunder function allows you to use this data structure in a loop.

        Usage: `for value in my_list:`

        Returns:
            An iterator that points to each value in the list using the `yield`
                statement.
        """
        if len(self) == 0:
            return

        cur_node = self.head
        while cur_node is not None:
            for x in cur_node.data_list:
                yield x
            cur_node = cur_node.next_node

    def __contains__(self, item):
        """ Returns True/False whether the list contains the given item

        Usage: `5 in my_list`

        Args:
            item: The object for which containment is being checked for.

        Returns:
            True: if `item` is found somewhere in the list
            False: if `item` is not found anywhere in the list
        """
        cur_node = self.head
        while cur_node is not None:
            if item in cur_node.data_list:
                return True
            else:
                cur_node = cur_node.next_node

        return False

    def append(self, data):
        """ Add a new object to the end of the list.

        This adds a new object, increasing the overall size of the list by 1.

        RULES FOR APPENDING (paraphrased from Wikipedia):
        To insert a new element, we simply find the node the element should be
        in and insert the element into the elements array, incrementing
        the size of the list. If the array is already full, we first insert a
        new node either preceding or following the current one and move half of
        the elements in the current node into it.

        For appending you should always create a new node at the end of the
        list.

        Usage: `my_list.append(4)`

        Args:
            data: The new object to be added to the list

        Returns:
            nothing

        """
        # If list is empty, create a new node
        if self.length == 0:
            self.head = self.Node([data], None)
            self.tail = self.head
        # Otherwise add to the end of the tail. If the tail
        # becomes unbalanced (grows beyond max_node_capacity)
        # then split it, creating a new tail.
        else:
            self.tail.append(data)
            if len(self.tail.data_list) > self.max_node_capacity:
                self.__split_node(self.tail)

        self.length += 1

    def __reversed__(self):
        """ Works just like __iter__, but starts from the back.

        Usage: `for i in reversed(my_list)`

        Returns:
            An iterator starting from the back of the list
        """
        if len(self) == 0:
            return

        # Create a list containing pointers to each
        # prev_node in the list.
        cur_node = self.head
        prev_nodes = [None]
        while cur_node != self.tail:
            prev_nodes.append(cur_node)
            cur_node = cur_node.next_node

        # Using the prev_nodes list, iterate backwards
        while cur_node is not None:
            for x in reversed(cur_node.data_list):
                yield x
            cur_node = prev_nodes[-1]
            del prev_nodes[-1]

    def __str__(self):
        """ Returns a string representation of the list.

        The format for representing an unrolled linked list will be as follows:
            - curly braces indicates an unrolled linked list
            - square brackets indicates a node
            - all values are separated by a comma and a space
        For example:
        {[1, 2, 3], [0, 9, 8], [2, 4, 6]}
        This list has three nodes and each node as three int objects in it.

        Usage: `str(my_list)`

        Returns:
            A string representation of the list.
        """
        cur_node = self.head
        str_list = ['{']
        while cur_node is not None:
            str_list.append(str(cur_node))
            if cur_node is not self.tail:
                str_list.append(', ')
            cur_node = cur_node.next_node
        str_list.append('}')
        return ''.join(str_list)

    def __verify_index(self, index):
        """Verifies that the given index is an int and is not out of bounds. If
        the index is valid then return True.
        """
        if not isinstance(index, int):
            raise TypeError("Index must be of type int")
        elif index >= self.length or index < -self.length:
            raise IndexError("Index out of bounds")
        return True

    def __find_node_index(self, index):
        """Finds the node and node list index that corresponds to the
        given index as well as the indexed node's previous node.
        """
        cur_index = 0
        cur_node = self.head
        prev_node = None
        while cur_node is not None:
            if index >= len(cur_node.data_list) + cur_index:
                cur_index += len(cur_node.data_list)
                prev_node = cur_node
                cur_node = cur_node.next_node
            else:
                index -= cur_index
                break
        return index, prev_node, cur_node

    def __insert(self, index, value):
        """
        """
        if not isinstance(value, UnrolledLinkedList):
            raise TypeError("Can only set an UnrolledLinkedList in a slice")

        if len(self) == 0:
            for x in value:
                self.append(x)
            return

        index, prev_node, cur_node = self.__find_node_index(index)
        for i, x in enumerate(value):
            cur_node.data_list.insert(index + i, x)

        self.length += value.length
        self.__balance_list()

    def __split_node(self, cur_node):
        """Creates a new node and splits the current contents of data_list evenly
        among them. The current node will point to the new node and the new node
        will point to the initial next_node
        """
        temp = self.Node(cur_node.data_list[len(cur_node.data_list) / 2:], cur_node.next_node)
        cur_node.data_list = cur_node.data_list[:len(cur_node.data_list) / 2]
        cur_node.next_node = temp

        if cur_node == self.tail:
            self.tail = cur_node.next_node

    def __balance_node(self, prev_node, cur_node):
        """Balances a node that has its list less than half-full.
        """
        if len(cur_node.data_list) == self.max_node_capacity / 2:
            return

        # node is empty?
        if not cur_node.data_list:
            self.__del_node(prev_node, cur_node)

        # node is not tail?
        elif cur_node != self.tail:
            if len(cur_node.next_node.data_list) - 1 < self.max_node_capacity / 2:
                cur_node.data_list += cur_node.next_node.data_list
                self.__del_node(cur_node, cur_node.next_node)
            else:
                cur_node.data_list.append(cur_node.next_node.data_list[0])
                del cur_node.next_node.data_list[0]
        elif len(cur_node.data_list) < self.max_node_capacity and prev_node is not None:
            prev_node.data_list.append(cur_node.data_list[0])
            del cur_node.data_list[0]
            self.__del_node(prev_node, cur_node)

    def __del_node(self, prev_node, cur_node):
        """Deletes the given node by pointing the previous node to the
        current node's next node
        """
        if len(self) == 0:
            self.head = None
            self.tail = None
        elif prev_node is None:
            self.head = cur_node.next_node
        else:
            prev_node.next_node = cur_node.next_node
            if cur_node == self.tail:
                self.tail = prev_node

    def __balance_list(self):
        """Balances the given UnrolledLinkedList by iterating over each node,
        balancing/splitting as necessary.
        """
        cur_node = self.head
        prev_node = None

        while cur_node is not None:
            if len(cur_node.data_list) > self.max_node_capacity:
                while len(cur_node.data_list) > self.max_node_capacity:
                    self.__split_node(cur_node)
            elif len(cur_node.data_list) < self.max_node_capacity / 2:
                self.__balance_node(prev_node, cur_node)
            prev_node = cur_node
            cur_node = cur_node.next_node

    @property
    def max_node_size(self):
        """Returns the specified max capacity for each node"""
        return self.max_node_capacity
