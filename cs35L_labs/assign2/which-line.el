(defun which-line ()
  "Print the current line number (in the buffer) of point."
  (interactive)
  (save-restriction
    (widen)
    (save-excursion
      (beginning-of-line)
     ;(defvar x (1+(count-lines 1 (point))))
     ;(defvar y (1+(count-lines 1 (window-end))))
     (message "Line %d of %d" ( 1+(count-lines 1 (point))) (1+(count-lines 1 (window-end))))
     )))

    
