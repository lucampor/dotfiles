;;; lisp/lcp-roam.el -*- lexical-binding: t; -*-
(defvar lcp/org-roam-changes-in-directory 't)
(defvar lcp/org-roam-selected-directory org-roam-directory)

;; (defun lcp/dir-parent-char-list (abs-path &optional parent-input)
;;   (seq-map
;;    #'(lambda (dir)
;;        (let* ((rel-path (f-relative dir org-roam-directory))
;;               (char (string-to-char (f-filename dir))))
;;          `(,parent-input ,char ,rel-path)))
;;    (f-directories abs-path)))

;; (defun lcp/capture-templates-input (&optional initial)
;;   (let ((pending-dirs (lcp/dir-parent-char-list (if initial initial org-roam-directory)))
;;         (parent-used-chars '())
;;         (templates '()))
;;     (while-let ((current (pop pending-dirs)))
;;       (cl-multiple-value-bind (parent-input raw-char dir-path) current
;;         (let* ((char (if (or 't; TODO repeated char for parent
;;                              (not raw-char))
;;                          raw-char
;;                        66
;;                        ;; TODO assign new char
;;                        ))
;;                (abs-path (concat org-roam-directory dir-path))
;;                (char-as-str (char-to-string char))
;;                (full-input (concat parent-input char-as-str)))
;;           (print abs-path)
;;           (print char-as-str)
;;           (print full-input)
;;           (let*
;;               (
;;                (new-dirs (lcp/dir-parent-char-list abs-path full-input)))
;;             (append pending-dirs new-dirs)
;;             (add-to-list parent-used-chars (cons parent-input char))
;;             (when (null new-dirs)
;;               (add-to-list templates `(,full-input ,dir-path))
;;               (add-to-list parent-used-chars (cons full-input char))
;;               (set 'full-input (concat full-input char-as-str)))
;;             (add-to-list templates `(,full-input ,dir-path plain "%?"
;;                                      :target (file+head ,(concat dir-path "/${slug}.org")
;;                                                         "#+title: ${title}\n")
;;                                      :jump-to-captured t
;;                                      :unnarrowed t))))))
;;     (print templates)))

(defun lcp/select-roam-dir ()
  (let* ((dir (read-directory-name "Select roam directory: "
                                   org-roam-directory
                                   org-roam-directory
                                   nil)))
    (when (f-ancestor-of-p org-roam-directory dir)
      (directory-file-name (f-relative dir org-roam-directory)))))

(defun lcp/org-roam-template (&optional dir-path)
  `(("r" "roam" plain "%?"
     :target (file+head ,(concat (when dir-path (concat dir-path "/")) "${slug}.org")
                        "#+title: ${title}\n#+startup: inlineimages content latexpreview\n")
     :jump-to-captured t
     :unnarrowed t)))

(defun lcp/org-roam-get-node-by-dir (node dir)
  (let ((cur (org-roam-node-dir node))
        (len (length dir)))
    (unless (> len (length cur))
      (string= dir
               (substring cur 0 len)))))

(defun lcp/org-roam-random-node ()
  (interactive)
  (let* ((selected (lcp/select-roam-dir))
         (dir (if selected selected
                lcp/org-roam-selected-directory)))
    (setq lcp/org-roam-selected-directory dir)
    (org-roam-node-random nil
                          (lambda (node)
                            (lcp/org-roam-get-node-by-dir node dir)))))

(defun lcp/org-roam-random-node-last-dir ()
  (interactive)
  (org-roam-node-random nil
                        (lambda (node)
                          (lcp/org-roam-get-node-by-dir node lcp/org-roam-selected-directory))))

(defun lcp/org-roam-select-and-insert ()
  (interactive)
  (let* ((selected (lcp/select-roam-dir))
         (dir (if selected selected
                lcp/org-roam-selected-directory)))
    (setq lcp/org-roam-selected-directory dir)
    (org-roam-node-insert (lambda (node)
                            (lcp/org-roam-get-node-by-dir node dir))
                          :templates (lcp/org-roam-template dir))))

(defun lcp/org-roam-search-last-dir ()
  (interactive)
  (org-roam-node-find nil nil
                      #'(lambda (node)
                          (lcp/org-roam-get-node-by-dir node lcp/org-roam-selected-directory))))

(defun lcp/org-roam-search-current ()
  (interactive)
  (lcp/org-roam-search 't))

(defun lcp/org-roam-search (&optional only-current)
  (interactive)
  (let* ((dir-path (lcp/select-roam-dir))
         (search-dir (if dir-path
                         dir-path
                       "*")))
    (print (concat dir-path " is the new initial search directory"))
    (setq lcp/org-roam-selected-directory search-dir)
    (setq org-roam-capture-templates (lcp/org-roam-template dir-path))
    (print dir-path)
    (org-roam-node-find nil nil
                        (lambda (node)
                          (if only-current (string= dir-path (org-roam-node-dir node))
                            (lcp/org-roam-get-node-by-dir node search-dir))))))

(provide 'lcp-roam)
