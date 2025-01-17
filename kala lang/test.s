;  (unrecognized syntax)
myList: .data 1, 2, 3, 4, 5
;  (unrecognized syntax)
mov $1, %rax
mov $1, %rdi
lea Welcome to Kala Language!, %rsi
syscall
;  (unrecognized syntax)
cmp myList[0] == 1, 0
je else_label
mov $1, %rax
mov $1, %rdi
lea First element is 1, %rsi
syscall
else_label:
;  (unrecognized syntax)
while_label:
cmp myList[0] < 10, 0
je end_while_label
mov $1, %rax
mov $1, %rdi
lea Incrementing first element, %rsi
syscall
; myList[0] = myList[0] + 1 (unrecognized syntax)
jmp while_label
end_while_label:
;  (unrecognized syntax)
mov 0, %i
for_label:
cmp %i,  5
jge end_for_label
mov $1, %rax
mov $1, %rdi
lea Index: , %rsi
syscall
mov $1, %rax
mov $1, %rdi
lea i, %rsi
syscall
jmp for_label
end_for_label:
;  (unrecognized syntax)
; Start of class MyClass
; Start of method greet()
mov $1, %rax
mov $1, %rdi
lea Hello from MyClass!, %rsi
syscall
; End of method greet()
; End of class MyClass
;  (unrecognized syntax)
; MyClass instance (unrecognized syntax)
; instance.greet() (unrecognized syntax)
