; ModuleID = "Module"
target triple = "unknown-unknown-unknown"
target datalayout = ""

@"pi" = global double 0x400921fafc8b007a
define double @"distance"()
{
start:
  %"vel" = alloca double
  %"time" = alloca double
  store double 0x401b851eb851eb85, double* %"vel"
  store double 0x4008000000000000, double* %"time"
  %".4" = load double, double* %"vel"
  %".5" = load double, double* %"time"
  %".6" = fmul double %".4", %".5"
  %"dist" = alloca double
  store double %".6", double* %"dist"
  %".8" = load double, double* %"dist"
  ret double %".8"
}

