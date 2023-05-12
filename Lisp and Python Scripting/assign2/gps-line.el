#!/bin/sh
(defun gps-line ()
  "Similar to `what-line` but also displays total number of lines in buffer."
  (interactive)
  (let ((current-line (line-number-at-pos))
	(total-lines (count-matches "\n" (point-min) (point-max))))
    (message "Line %d/%d" current-line total-lines)))
