(function() {
  (function($) {
        return $.widget("IKS.anchor", {
            options: {
              editable: null,
              uuid: "",
              link: true,
              image: true,
              defaultUrl: '',
              dialogOpts: {
                autoOpen: false,
                width: 800,
                height: 300,
                title: "Insert anchor",
                buttonTitle: "Insert",
                buttonUpdateTitle: "Update",
                modal: true,
                resizable: false,
                draggable: false,
                dialogClass: 'hallolink-dialog'
              },
              buttonCssClass: null
            },
            populateToolbar: function(toolbar) {
              var butTitle, butUpdateTitle, buttonize, buttonset, dialog, dialogId, dialogSubmitCb, isEmptyLink, urlInput, selectInput, widget, headings;
              widget = this;
              dialogId = "" + this.options.uuid + "-dialog";
              butTitle = this.options.dialogOpts.buttonTitle;
              butUpdateTitle = this.options.dialogOpts.buttonUpdateTitle;
              headings = $(window)[0].halloPlugins.halloheadings.formatBlocks;

              dialog = "<div id=\"" + dialogId + "\"><form action=\"#\" method=\"post\" class=\"linkForm\"><ul class=\"fields\">";
              dialog += "<li class=\"required\"><div class=\"field\"><label for=\"anchor-type\">HTML tag:</label><div class=\"field-content\"><select id=\"anchor-type\" name=\"anchor-type\">";
              for (var i = headings.length - 1; i >= 0; i--) {
                if (headings[i] !== "p")
                  dialog += "<option value=\"" + headings[i] +"\">" + headings[i] + "</option>";
              }
              dialog += "<span>::after</span></select></div></div></li>";
              dialog += "<li class=\"required\"><div class=\"field\"><label for=\"anchor-name\">Name:</label><div class=\"field-content\"><input id=\"anchor-name\" class=\"url\" type=\"text\" name=\"url\" value=\"" + this.options.defaultUrl + "\" />";
              dialog += "</div></div></li>";
              dialog += "<li><input type=\"submit\" id=\"addlinkButton\" value=\"" + butTitle + "\"/></li>";
              dialog += "</ul></form></div>";
              dialog = jQuery(dialog);
              urlInput = jQuery('input[name=url]', dialog);
              selectInput = jQuery('select[name=anchor-type]', dialog);

              isAnchorValid = function() {
                if (!$(urlInput).val() || !$(selectInput).val())
                  return false;
                else
                  return true;
              };

              getEnclosingAnchorElement = function() {
                var node;
                node = widget.options.editable.getSelection().commonAncestorContainer;

                if (jQuery.inArray($(node).parent().prop('tagName'), headings) && $(node).parents().get(0).id.length > 0 )
                  return $(node).parents().get(0);
                else
                  return false;

              };

              isEmptyLink = function(link) {
                if ((new RegExp(/^\s*$/)).test(link)) {
                  return true;
                }
                if (link === widget.options.defaultUrl) {
                  return true;
                }
                return false;
              };
              dialogSubmitCb = function(event) {
                if (isAnchorValid()) {
                  var link, linkNode;
                  event.preventDefault();
                  link = urlInput.val();
                  dialog.dialog('close');
                  widget.options.editable.restoreSelection(widget.lastSelection);
                  
                  var insertionPoint, lastSelection;

                  lastSelection = widget.options.editable.getSelection();
                  insertionPoint = $(lastSelection.endContainer).parentsUntil('.richtext').last();
                  var elem;
                  elem = "<" + selectInput.val() + " id='" + link + "'>" + lastSelection + "</" + selectInput.val() + ">";
                  var node = lastSelection.createContextualFragment(elem);
              
                  lastSelection.deleteContents();
                  lastSelection.insertNode(node);
      
                  widget.options.editable.element.trigger('change');
                }
                return false;
              };
              dialog.find("input[type=submit]").click(dialogSubmitCb);
              buttonset = jQuery("<span class=\"" + widget.widgetName + "\"></span>");
              buttonize = (function(_this) {
                return function(type) {
                  var button, buttonHolder, id;
                  id = "" + _this.options.uuid + "-" + type;
                  buttonHolder = jQuery('<span></span>');
                  buttonHolder.hallobutton({
                    label: 'Anchor',
                    icon: 'fa fa-anchor',
                    editable: _this.options.editable,
                    command: null,
                    queryState: function(event) {
                      return button.hallobutton('checked', !!getEnclosingAnchorElement());
                    },
                    uuid: _this.options.uuid,
                    cssClass: _this.options.buttonCssClass
                  });
                  buttonset.append(buttonHolder);
                  button = buttonHolder;
                  button.on("click", function(event) {
                    var button_selector, selectionParent;
                    widget.lastSelection = widget.options.editable.getSelection();
                    urlInput = jQuery('input[name=url]', dialog);
                    selectionParent = widget.lastSelection.startContainer.parentNode;
                    if (!selectionParent.id) {
                      urlInput.val(widget.options.defaultUrl);
                      jQuery(urlInput[0].form).find('input[type=submit]').val(butTitle);
                    } else {
                      urlInput.val(jQuery(selectionParent).attr('id'));
                      button_selector = 'input[type=submit]';
                      jQuery(urlInput[0].form).find(button_selector).val(butUpdateTitle);
                    }
                    widget.options.editable.keepActivated(true);
                    dialog.dialog('open');
                    dialog.on('dialogclose', function() {
                      widget.options.editable.restoreSelection(widget.lastSelection);
                      jQuery('label', buttonHolder).removeClass('ui-state-active');
                      widget.options.editable.element.focus();
                      return widget.options.editable.keepActivated(false);
                    });
                    return false;
                  });
                  return _this.element.on("keyup paste change mouseup", function(event) {
                    var nodeName, start;
                    start = jQuery(widget.options.editable.getSelection().startContainer);
                    if (start.prop('nodeName')) {
                      nodeName = start.prop('nodeName');
                    } else {
                      nodeName = start.parent().prop('nodeName');
                    }
                    if (nodeName && nodeName.toUpperCase() === "A") {
                      jQuery('label', button).addClass('ui-state-active');
                      return;
                    }
                    return jQuery('label', button).removeClass('ui-state-active');
                  });
                };
              })(this);
              if (this.options.link) {
                buttonize("A");
              }
              if (this.options.link) {
                toolbar.append(buttonset);
                buttonset.hallobuttonset();
                return dialog.dialog(this.options.dialogOpts);
              }
            }
          });
        })(jQuery);

}).call(this);


(function() {
  (function($) {
    return $.widget("IKS.anchorlink", {
      options: {
        editable: null,
        uuid: "",
        link: true,
        image: true,
        defaultUrl: '',
        dialogOpts: {
          autoOpen: false,
          width: 540,
          height: 250,
          title: "Enter Anchor Link",
          buttonTitle: "Insert Anchor Link",
          buttonUpdateTitle: "Update",
          modal: true,
          resizable: false,
          draggable: false,
          dialogClass: 'hallolink-dialog'
        },
        buttonCssClass: null
      },
      populateToolbar: function(toolbar) {
        var butTitle, butUpdateTitle, buttonize, buttonset, dialog, dialogId, dialogSubmitCb, isEmptyLink, urlInput, widget;
        widget = this;
        getEnclosingAnchorLink = function() {
          var node;
          node = widget.options.editable.getSelection().commonAncestorContainer;
          return $(node).parents("a[href^='#']").get(0);
        };

        dialogId = "" + this.options.uuid + "-dialog";
        butTitle = this.options.dialogOpts.buttonTitle;
        butUpdateTitle = this.options.dialogOpts.buttonUpdateTitle;
        dialog = "<div id=\"" + dialogId + "\"> <form action=\"#\" method=\"post\" class=\"linkForm\"><ul class=\"fields\">";
        dialog += "<li class=\"required\"><div class=\"field\"><label for=\"anchor-type\">Link to:</label><div class=\"field-content\">";
        dialog += "<input class=\"url\" type=\"text\" name=\"url\" value=\"" + this.options.defaultUrl + "\" />";
        dialog += "</div></div></li>";
        dialog += "<li><input type=\"submit\" id=\"addlinkButton\" value=\"" + butTitle + "\"/></li>";
        dialog += "</ul></form></div>";
        dialog = jQuery(dialog);

        urlInput = jQuery('input[name=url]', dialog);
        isEmptyLink = function(link) {
          if ((new RegExp(/^\s*$/)).test(link)) {
            return true;
          }
          if (link === widget.options.defaultUrl) {
            return true;
          }
          return false;
        };
        dialogSubmitCb = function(event) {
          var link, linkNode;
          event.preventDefault();
          link = urlInput.val();
          dialog.dialog('close');
          widget.options.editable.restoreSelection(widget.lastSelection);
          if (isEmptyLink(link)) {
            document.execCommand("unlink", null, "");
          } else {
            
            if (widget.lastSelection.startContainer.parentNode.href === void 0) {
              if (widget.lastSelection.collapsed) {
                linkNode = jQuery("<a href='#" + link + "'>" + link + "</a>")[0];
                widget.lastSelection.insertNode(linkNode);
              } else {
                document.execCommand("createLink", null, "#" + link);
              }
            } else {
              widget.lastSelection.startContainer.parentNode.href = "#" + link;
            }
          }
          widget.options.editable.element.trigger('change');
          return false;
        };
        dialog.find("input[type=submit]").click(dialogSubmitCb);
        buttonset = jQuery("<span class=\"" + widget.widgetName + "\"></span>");
        buttonize = (function(_this) {
          return function(type) {
            var button, buttonHolder, id;
            id = "" + _this.options.uuid + "-" + type;
            buttonHolder = jQuery('<span></span>');
            buttonHolder.hallobutton({
              label: 'Anchor Link',
              icon: 'fa fa-external-link-square',
              editable: _this.options.editable,
              command: null,
              queryState: function(event) {
                return button.hallobutton('checked', !!getEnclosingAnchorLink());
              },
              uuid: _this.options.uuid,
              cssClass: _this.options.buttonCssClass
            });
            buttonset.append(buttonHolder);
            button = buttonHolder;
            button.on("click", function(event) {
              var button_selector, selectionParent;
              widget.lastSelection = widget.options.editable.getSelection();
              urlInput = jQuery('input[name=url]', dialog);
              selectionParent = widget.lastSelection.startContainer.parentNode;
              if (!selectionParent.href) {
                urlInput.val(widget.options.defaultUrl);
                jQuery(urlInput[0].form).find('input[type=submit]').val(butTitle);
              } else {
                urlInput.val(jQuery(selectionParent).attr('href').substring(1));
                button_selector = 'input[type=submit]';
                jQuery(urlInput[0].form).find(button_selector).val(butUpdateTitle);
              }
              widget.options.editable.keepActivated(true);
              dialog.dialog('open');
              dialog.on('dialogclose', function() {
                widget.options.editable.restoreSelection(widget.lastSelection);
                jQuery('label', buttonHolder).removeClass('ui-state-active');
                widget.options.editable.element.focus();
                return widget.options.editable.keepActivated(false);
              });
              return false;
            });
            return _this.element.on("keyup paste change mouseup", function(event) {
              var nodeName, start;
              start = jQuery(widget.options.editable.getSelection().startContainer);
              if (start.prop('nodeName')) {
                nodeName = start.prop('nodeName');
              } else {
                nodeName = start.parent().prop('nodeName');
              }
              if (nodeName && nodeName.toUpperCase() === "A") {
                jQuery('label', button).addClass('ui-state-active');
                return;
              }
              return jQuery('label', button).removeClass('ui-state-active');
            });
          };
        })(this);
        if (this.options.link) {
          buttonize("A");
        }
        if (this.options.link) {
          toolbar.append(buttonset);
          buttonset.hallobuttonset();
          return dialog.dialog(this.options.dialogOpts);
        }
      }
    });
  })(jQuery);
}).call(this);
