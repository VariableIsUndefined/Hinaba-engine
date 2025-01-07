% from bottle import ConfigDict
% from json import loads
% config = ConfigDict()
% config.load_config('imageboard.conf')
% report_reasons = loads(config['reports.reasons'])
% styles = loads(config['style.styles'])

<div class="bottomCtrl">
  <span class="deleteform">
    Delete Post: <input type="submit" value="Delete"></td>
  </span>
  <span>
    <select name="report">
    <option selected disabled>Reason:</option>
    % for reason in report_reasons:
      <option value="{{reason}}">{{reason}}</option>   
    % end
    </select>
    <input type="submit" value="Report">
  </span>
  <span class="stylechanger">
    Style: <select id="styleSelector" onchange="changeStyle(this.value)">>
      % for s in styles:
        % if style == s:
          <option value="{{s}}" selected>{{s}}</option>
        % else:
          <option value="{{s}}">{{s}}</option>
        % end
      % end
    </select>
  </span>
</div>
