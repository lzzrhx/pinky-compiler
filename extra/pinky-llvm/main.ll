; ModuleID = "pinky_subset"
target triple = "unknown-unknown-unknown"
target datalayout = ""

define i32 @"main"()
{
.2:
  %".3" = fneg double 0x4014000000000000
  %".4" = fmul double 0x4012666666666666, %".3"
  %".5" = fadd double 0x4059000000000000, %".4"
  %".6" = fneg double 0x4000000000000000
  %".7" = fsub double %".5", %".6"
  %".8" = fdiv double 0x4003333333333333, 0x4000000000000000
  %".9" = fadd double %".7", %".8"
  call void @"print_f64"(double %".9")
  %".11" = fadd double 0x402acccccccccccd, 0x4000000000000000
  %".12" = alloca double
  store double %".11", double* %".12"
  %".14" = load double, double* %".12"
  call void @"print_f64"(double %".14")
  %".16" = fadd double 0x402acccccccccccd, 0x4000000000000000
  store double %".16", double* %".12"
  %".18" = load double, double* %".12"
  %".19" = fcmp ogt double %".18",              0x0
  br i1 %".19", label %".20", label %".21"
.20:
  call void @"print_f64"(double 0x3ff0000000000000)
  br label %".22"
.21:
  call void @"print_f64"(double              0x0)
  br label %".22"
.22:
  %".28" = alloca double
  store double 0x3ff0000000000000, double* %".28"
  br label %".30"
.30:
  %".34" = load double, double* %".28"
  %".35" = fcmp ole double %".34", 0x4024000000000000
  br i1 %".35", label %".31", label %".32"
.31:
  %".37" = load double, double* %".28"
  %".38" = frem double %".37", 0x4000000000000000
  %".39" = fcmp oeq double %".38",              0x0
  br i1 %".39", label %".40", label %".41"
.32:
  ret i32 0
.40:
  %".44" = load double, double* %".28"
  call void @"print_f64"(double %".44")
  br label %".42"
.41:
  br label %".42"
.42:
  %".48" = load double, double* %".28"
  %".49" = fadd double %".48", 0x3ff0000000000000
  store double %".49", double* %".28"
  br label %".30"
}

declare void @"print_i32"(i32 %".1")

declare void @"print_f64"(double %".1")

declare void @"print_i1"(i1 %".1")
