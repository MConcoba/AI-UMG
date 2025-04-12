curso(Cid, ca1, Nombre, _, _).
carrera(CA, ingenieria_en_sistemas) , curso(C, CA, Nombre, _, _).



asignacion(e1, _, C), curso(C, _, _, Ciclo, _), ciclo(Ciclo, NombreCiclo, _).
ciclos_estudiante(e1, Ciclos).


prerequisitos_curso(cu5, Prerrequisito).
curso(cu5, _, _, _, Prerrequisito).
curso(cu5, _, _, _, Prerrequisito), Prerrequisito \= n, curso(Prerrequisito, _, NombreCurso, _, _). 

