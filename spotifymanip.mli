module type CELL = sig 
  (* type 'a cell of cells containing a value of type 'a *)
  type 'a cell
  (* type 'a exp of expressions returning a value of type 'a *)
  type 'a exp

  val return : 'a -> 'a exp
  val (>>=) : 'a exp -> ('a -> 'b exp) -> 'b exp
  val cell : 'a exp -> 'a cell exp 
  val get :  'a cell -> 'a exp
  val set : 'a cell -> 'a exp -> unit 
  val run : 'a exp -> 'a 
end

