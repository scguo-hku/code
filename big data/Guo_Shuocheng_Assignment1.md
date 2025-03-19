# Q1

## (a)

### (1)

$$
\pi_{\text{title}} \left( \sigma_{\text{genre} = ' \text{Novel} ' \land \text{language} = ' \text{Chinese} '} ({Book}) \right)
$$



### (2)

$$
\pi_{name}(\sigma_{gender='Ms.' \land dueDate='01-01-2025'}((Customer \bowtie Borrow) \bowtie (\sigma_{genre='Novel'}(Book)))
$$



## (b)

### (1)

```sql
SELECT DISTINCT B.genre
FROM Customer C
JOIN Borrow Br ON C.cID = Br.cID
JOIN Book B ON Br.bID = B.bID
WHERE C.gender = 'Mr.' AND C.age BETWEEN 40 AND 60;
```

### (2)

```sql
SELECT B.genre, AVG(C.age) AS average_age
FROM Customer C
JOIN Borrow Br ON C.cID = Br.cID
JOIN Book B ON Br.bID = B.bID
GROUP BY B.genre;
```



# Q2

## (1)

| Access action | Content of Q after access action                             |
| ------------- | ------------------------------------------------------------ |
| visit root    | M1(1), M2(2), M3(4)                                          |
| access M1     | m2($ \sqrt{2} $), m1(2), M2(2), M3(4)                        |
| access m2     | a($ \sqrt{2} $), m1(2), M2(2), b($\sqrt{5}$), c($\sqrt{8}$), M3(4) |
| access a      | Dissatisfaction                                              |
| access m1     | M2(2), b($\sqrt{5}$), e($\sqrt{5}$), c($\sqrt{8}$),  d(4),  M3(4) |
| access M2     | m3(2), b($\sqrt{5}$), e($\sqrt{5}$), c($\sqrt{8}$), m4(4), M3(4) |
| access m3     | f(2), b($\sqrt{5}$), e($\sqrt{5}$),c($\sqrt{8}$), g($\sqrt{10}$), m4(4), M3(4) |
| access f      | 7 > 6, satisfaction                                          |

## (2)

**Building f** is the closest valid building.

Nodes Accessed: **8**(root, M1, m2, a, m1, M2, m3, f).



