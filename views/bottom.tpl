% from bottle import ConfigDict
% from json import loads
% config = ConfigDict()
% config.load_config('imageboard.conf')
% report_reasons = loads(config['reports.reasons'])

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
</div>
