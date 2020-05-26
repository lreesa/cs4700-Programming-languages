

# (set a 1)
# (+ 7 a)
# (def my+ (x y)
#      (+ x y))
# (my+ 1 2)
#      
 (set a (quote (1)))
# # (rest a)
# # (first a)
# # (atom a)
# # (atom (rest a))
# 
 (set b (cons (first a)(rest a)))
# # b
# # 
# # (atom nil)
# # (atom 1)
# 
# # (def length (list)
# #    (if (atom list)
# #         0
# #         (+ 1 (length (rest list)))))
# # (set ba (quote (1)))
# # (length ba)
# # 
# # (+ 5 6)
# # 
# # # test assignment
# # (set x (+ 5 6))
# # (set y (- 3 5))
# # # test lookup
# # (set y (+ 5 x)) 
# # 
# # #test functions
# # (set x 10) 
# # x
# # (def f (x y) 
# #     (+ x y))
# # (f 2 1)
# # 
# # (set y 10) 
# # (f x y)
# # 
# (set y 3)
            
(def fact (x) 
    (if (eq x 1) 
        x 
        (* x (fact (- x 1)))))

# (+ (fact y) y)
              
# (set x 12)

(def fib (x) 
    (if (< x 0) 
        0 
        (if (or (eq x 2) 
        (eq x 1)) 
            x 
            (+ (fib (- x 2)) 
                (fib (- x 1))))))
                
# (+ (fib 5) (fib x))
          
# (first (quote (1 2 3)))

# (cons (quote 1111) (quote (1 2 3)))

# (set l (quote nil))
# (set q (quote (1 2)))
# (set p (quote (3 4)))
# (set a (quote ((3 4)(5 6))))
# (set b (quote ((3 4)(5 7))))

(def listp (a) 
    (not (atom a)))

# (set x 1)
# (set q (quote (x 2)))
# (set p (quote (1 4)))
# # tests that two nested lists are the same structure with the same contents
(def equal (a b)
    (if (eq a b) 
        True 
        (if (or (not (listp a)) 
                (not (listp b))) 
            False 
            (and (equal (first a) (first b)) 
                  (equal (rest a) (rest b))))))
# (equal q p)

# p
              
# (equal l p)
# (equal a a)
# (equal a b)
# (equal l b)
# generates a list of acending numbers        
(def generateList (a) 
    (if (eq a 0) 
        nil
        (cons a (generateList (- a 1)))))
        
# (generateList 2)
# (generateList 33)

# remove the item from a list at i index
(def removeIndex (i list) 
    (if (eq i 0) 
        (rest list) 
        (if (eq list nil)
            nil
            (cons (first list) 
                  (removeIndex (- i 1) 
                                (rest list))))))
              
# (removeIndex 2 (generateList 6))
# (removeIndex 5 (generateList 6))
# (removeIndex 15 (generateList 6))

#remove val from list if it is in there
(def removeValue (val list) 
    (if (eq val (first list)) 
        (rest list) 
        (cons (first list) 
              (removeValue val (rest list)))))
              
# (removeValue 2 (generateList 20))
# (removeValue 6 (generateList 20))

#return true if val is in tree 
(def valInTree (val tree) 
    (if (eq tree nil)
        False
        (if (eq val (first tree)) 
            True 
                (valInTree val (rest tree)))))

# (valInTree 1 b)
# (valInTree 30 b)

#appends two lists together
(def append (list0 list1) 
    (if (eq list0 nil) 
        list1 
        (cons (first list0) 
              (append (rest list0) list1))))
              
# (append (generateList 4) (generateList 5))

(def reverseList (list) 
    (if (eq list nil)
        nil
        (append (reverseList (rest list))
                (cons (first list) nil))))

# helper function returns the ith item from list
(def get (i list) 
    (if (eq 0 i) 
        (first list) 
        (if (eq list nil)
            nil
            (get (- i 1) 
                  (rest list)))))
#helper function:  inserts value into ith position of list
(def insert (val i liststart listend) 
    (if (eq 0 i)) 
        (cons liststart (cons (quote val) (rest listend)))
        (if (eq listend nil))
            nil
            (insert val (- i 1) (cons liststart (first listend)) (rest listend)))
              
# takes an integer and binary tree and returns tree with integer inserted
( def insertNode (val list index)
    (if (eq list nil))
        (cons (quote val) list)
        (if (eq (get index list) nil))
            (insert val index nil list)
            (if (< val (first list)))
                    (insertNode val list (* 2 index))
                    (insertNode val list (+ 1 (* 2 index))))

# (insertNode 1 nil 0)
# (insertNode 1 b 0)

# for counting the number of ways to get a dice throw
# from the 5050 class
# n is the number of six sided dice
# x is the target
(def count (n x) 
    (if (eq n 0) 
        (if (eq x 0) 
            1
            0)
        (countEach n x 6)))

# helper function that counts down the faces
(def countEach (n x face) 
    (if (eq face 0) 
        0 
        (+ (count (- n 1) 
                  (- x face))
            (countEach n x (- face 1)))))
            
# (count 3 13)

# (set b 3)
# (def nonLocal (n)
#     (+ n b))
# (nonLocal 1)

 (+ True False)
 (eq True 1)

# (def test (x)
#    (+ x 12))


# (def testPass (func x)
#     (+ (func 22) (test x)))
# (testPass test 0)

# # 
