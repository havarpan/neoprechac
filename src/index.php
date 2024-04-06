<?php
if (!empty($_GET)){
    if (!empty($_GET["fbclid"])) {
            header('Location: https://neoprechac.org', true, 303);
            die();
    }
}
echo <<<EOD
<!DOCTYPE html>
<html>
<head>
    <title>PrechacThis</title>
    <meta http-equiv="Content-Type" content="text/html;charset=utf-8">
    <link rel="shortcut icon" href="./images/favicon.png">
    <link rel="stylesheet" type="text/css" href="./css/prechacthis.css">
</head>
<body>
EOD;

$debug = false;

if (!empty($_GET)){
	if (!empty($_GET["debug"])) {
        if($_GET["debug"]=="on") $debug = true;
	}
    $doku = doku($_GET["doku"]??false);
    if(!empty($doku)){
            echo <<<EOD
            <table align='center' cellpadding='0'>
                <tr>
                    <td class='classictd'>&nbsp;</td><td>Classic</td>
                    <td>&nbsp;-&nbsp;</td>
                    <td class='equitd'>&nbsp;</td><td>Equihanded</td>
                    <td>&nbsp;-&nbsp;</td>
                    <td class='bitd'>&nbsp;</td><td>Bi</td>
                    <td>&nbsp;-&nbsp;</td>
                    <td class='instantbitd'>&nbsp;</td><td>Instant Bi</td>
                </tr>
            </table><br>
            EOD;
    }

    echo "<table align='center' cellpadding='0'><tr><td>";

    if (empty($_GET["objects"])){$_GET["objects"] = "3;4;5;6;7";}
    $_GET["objects"] = str_replace(";", "or", $_GET["objects"]);
    $objects = explode("or", $_GET["objects"]);
    
    if (empty($_GET["lengths"])){$_GET["lengths"] = "2;3;4;5;6;8";}
    $_GET["lengths"] = str_replace(";", "or", $_GET["lengths"]);
    $lengths = explode("or", $_GET["lengths"]);
    
    if ($_GET["persons"]){echo "<h2>" . $_GET["persons"] . " persons</h2>";}

    if (empty($_GET["multiplex"])){$_GET["multiplex"] = "0";}

    if (empty($_GET["results"])){$_GET["results"] = 42;}
    
    if (empty($_GET["magic"])){$_GET["magic"] = 0;}
    else {$magicChecked = "'checked'";}
    
    $back_url = rawurlencode(htmlspecialchars($_SERVER["QUERY_STRING"]));
    
    foreach($objects as $object){
        foreach($lengths as $length){
            $errorlogfile = tempnam("/tmp", "siteswap");
    
            $plquery  = "swipl -q "
                              // flags outdated or unavailable, seems to work without them (havarpan Feb 27 2024)
                              // . "-L5M " // local stack size to 5 MB
                              // . "-G12M " // global stack size to 12 MB
                              // . "-T5M " // trail stack size to 5 MB
                              // . "-A2M " // argutment stack size to 2 MB
                              . "-f " . dirname($_SERVER["SCRIPT_FILENAME"]) . "/pl/siteswap.pl "
                              . "-g \"allSiteswaps("
                              . ($_GET["persons"]??"") . ", "
                              . "$object, "
                              . "$length, "
                              . ($_GET["max"]??"") . ", "
                              . ($_GET["multiplex"]??"") . ", "
                              . correctPasses(($_GET["passesmin"]??"")) . ", "
                              . correctPasses(($_GET["passesmax"]??"")) . ", "
                              . "\\\"". ($_GET["jugglerdoes"]??"") . "\\\", "
                              . "\\\"". ($_GET["exclude"]??"") . "\\\", "
                              . "\\\"". ($_GET["clubdoes"]??"") . "\\\", "
                              . "\\\"". ($_GET["react"]??"") . "\\\", "
							  . ($_GET["magic"]??"") . ", "
                              . ($_GET["results"]??"") . ", "
                              . "'". $back_url ."'"
                              . "), halt.\" "
                              . "2> $errorlogfile";
            
                    echo "<div class='inline'><div class='swaps'>";
                    echo "<h3>$object objects, ";
                    echo "period $length:</h3>";
                    if ($debug) echo "$plquery<br>\n";
                    echo `$plquery`;
                    readfile($errorlogfile);
                    unlink($errorlogfile);
                    echo "</div></div>";
                    
                }//lengths
            }//objects
            echo "</td></tr></table>";
        }

        if (!empty($doku) || count($_GET) == 0) {

            //default values
            if (empty($_GET["persons"])){$_GET["persons"] = 2;}
            $personsSelected[$_GET["persons"]] = "selected='selected'";
    
            if (empty($_GET["multiplex"])){$_GET["multiplex"] = 0;}
            $multiplexSelected[$_GET["multiplex"]] = "selected='selected'";
    
            if (empty($_GET["max"])){$_GET["max"] = 4;}
            $maxSelected[$_GET["max"]] = "selected='selected'";
    
            if (!isset($_GET["passesmin"])){$_GET["passesmin"] = 1;}
            $minPassSelected[$_GET["passesmin"]] = "selected='selected'";
    
            if (!isset($_GET["passesmax"]) or !is_numeric($_GET["passesmax"])){$_GET["passesmax"] = 0;}
            $maxPassSelected[$_GET["passesmax"]] = "selected='selected'";
    
            $hidden_debug="";
            if ($debug) $hidden_debug = "<input type='hidden' name='debug' value='on'>";
    
            echo "<form action='./index.php' method='get'>
             <p>&nbsp;<a href='https://github.com/havarpan/neoprechac' target='_blank'>source code &amp; info</a></p>
             <table align='center' cellpadding='10'>
              <tr>
               <td class='lable'></td>
    		   <td class='input'></td>";
    		   if (!empty($doku['head'])) {
    				   echo $doku["head"];
    		   }
    		  echo "
              </tr>
              <tr>
               <td class='lable'>Jugglers:</td>
               <td class='input'>
                <select name='persons' size='1'>
                 <option value='1'" . ($personsSelected[1] ?? "") . ">1</option>
                 <option value='2'" . ($personsSelected[2] ?? "") . ">2</option>
                 <option value='3'" . ($personsSelected[3] ?? "") . ">3</option>
                 <option value='4'" . ($personsSelected[4] ?? "") . ">4</option>
                 <option value='5'" . ($personsSelected[5] ?? "") . ">5</option>
                 <option value='6'" . ($personsSelected[6] ?? "") . ">6</option>
                 <option value='7'" . ($personsSelected[7] ?? "") . ">7</option>
                 <option value='8'" . ($personsSelected[8] ?? "") . ">8</option>
                 <option value='9'" . ($personsSelected[9] ?? "") . ">9</option>
                 <option value='10'" . ($personsSelected[10] ?? "") . ">10</option>
                </select>
               </td>";
               if (!empty($doku['persons'])) {
    			   echo $doku['persons'];
    		   }
    		   echo"
              </tr>
              <tr>
               <td class='lable'>Objects:</td>
    		   <td class='input'><input type='text' name='objects' value='";
    		   if (!empty($_GET['objects'])) { 
    				   echo $_GET['objects'];
    		   }
               echo "'></td>";
               if (!empty($doku['objects'])) {
                   echo $doku['objects'];
               }
              echo "
              </tr>
              <tr>
               <td class='lable'>Period:</td>
    		   <td class='input'><input type='text' name='lengths' value='";
    		   if (!empty($_GET['lengths'])) { 
    				   echo $_GET['lengths'];
    		   }
               echo "'></td>";
               if (!empty($doku['length'])) {
                   echo $doku['length'];
    		   }
              echo "
              </tr>
              <tr>
               <td class='lable'>Max height:</td>
               <td class='input'>
                <select name='max' size='1'>
                 <option value='1'" . ($maxSelected[1]??"") . ">1</option>
                 <option value='2'" . ($maxSelected[2]??"") . ">2</option>
                 <option value='3'" . ($maxSelected[3]??"") . ">3</option>
                 <option value='4'" . ($maxSelected[4]??"") . ">4</option>
                 <option value='5'" . ($maxSelected[5]??"") . ">5</option>
                 <option value='6'" . ($maxSelected[6]??"") . ">6</option>
                 <option value='7'" . ($maxSelected[7]??"") . ">7</option>
                 <option value='8'" . ($maxSelected[8]??"") . ">8</option>
                </select>
               </td>";
               if (!empty($doku['max'])) {
                   echo $doku['max'];
    		   }
               echo " 
              </tr>
              <tr>
               <td class='lable'>Passes</td>
               <td class='input'>
                min:
                <select name='passesmin' size='1'>
                 <option value='0'" . ($minPassSelected[0]??"") . ">0</option>
                 <option value='1'" . ($minPassSelected[1]??"") . ">1</option>
                 <option value='2'" . ($minPassSelected[2]??"") . ">2</option>
                 <option value='3'" . ($minPassSelected[3]??"") . ">3</option>
                 <option value='4'" . ($minPassSelected[4]??"") . ">4</option>
                 <option value='5'" . ($minPassSelected[5]??"") . ">5</option>
                 <option value='6'" . ($minPassSelected[6]??"") . ">6</option>
                 <option value='7'" . ($minPassSelected[7]??"") . ">7</option>
                 <option value='8'" . ($minPassSelected[8]??"") . ">8</option>
                </select>
                max:
                <select name='passesmax' size='1'>
                 <option value='1'" . ($maxPassSelected[1]??"") . ">1</option>
                 <option value='2'" . ($maxPassSelected[2]??"") . ">2</option>
                 <option value='3'" . ($maxPassSelected[3]??"") . ">3</option>
                 <option value='4'" . ($maxPassSelected[4]??"") . ">4</option>
                 <option value='5'" . ($maxPassSelected[5]??"") . ">5</option>
                 <option value='6'" . ($maxPassSelected[6]??"") . ">6</option>
                 <option value='7'" . ($maxPassSelected[7]??"") . ">7</option>
                 <option value='8'" . ($maxPassSelected[8]??"") . ">8</option>
                 <option value='_'" . ($maxPassSelected[0]??"") . ">&nbsp;</option>
                </select>
               </td>
              </tr>";
            /*  <tr>
               <td class='lable'>Multiplexes:</td>
               <td class='input'>
                <select name='multiplex' size='1'>
                 <option $multiplexSelected[0]>0</option>
                 <option $multiplexSelected[1]>1</option>
                 <option $multiplexSelected[2]>2</option>
                 <option $multiplexSelected[3]>3</option>
                 <option $multiplexSelected[4]>4</option>
                </select>
               </td>
               $doku[multiplex]
              </tr>*/
              echo "<tr>
               <td class='lable'>Contain:</td>
    		   <td class='input'><input type='text' name='jugglerdoes' value='";
    		   if (!empty($_GET['jugglerdoes'])) {
    				   echo $_GET['jugglerdoes'];
    		   }
               echo "'></td>";
               if (!empty($doku['contain'])) {
                   echo $doku['contain'];
               }
              echo "
              </tr>
              <tr>
               <td class='lable'>Exclude:</td>
    		   <td class='input'><input type='text' name='exclude' value='";
    		   if (!empty($_GET['exclude'])) {
    				   echo $_GET['exclude'];
    		   }
               echo "'></td>";
               if (!empty($doku['exclude'])) {
                   echo $doku['exclude'];
               }
              echo "
              </tr>
              <tr>
               <td class='lable'>Club does:</td>
    		   <td class='input'><input type='text' name='clubdoes' value='";
    		   if (!empty($_GET['clubdoes'])) {
    				   echo $_GET['clubdoes'];
    		   }
               echo "'></td>";
               if (!empty($doku['clubdoes'])) {
                   echo $doku['clubdoes'];
               }
              echo "
              </tr>
              <tr>
               <td class='lable'>React:</td>
    		   <td class='input'><input type='text' name='react' value='";
               if (!empty($_GET['react'])) {
                   echo $_GET['react'];
               }
              echo "'></td>";
               if (!empty($doku['react'])) {
                   echo $doku['react'];
               }
              echo "
              </tr>
              <tr>
               <td class='lable'>Contain magic:</td>
    		   <td class='input'><input type='checkbox' name='magic' value='1'";
               if (!empty($magicChecked)) {
    		       echo $magicChecked;
    		   }
               echo "></td>";
               if (!empty($doku['magic'])) {
                   echo $doku['magic'];
               }
              echo "
              </tr>
              <tr>
               <td class='lable'>Max results:</td>
    		   <td class='input'><input type='text' name='results' value='";
    		   if (!empty($_GET['results'])) {
                       echo $_GET['results'];
               }
               echo "'></td>";
               if (!empty($doku['results'])) {
                   echo $doku['results'];
               }
              echo "
              </tr>
    
              <tr>
               <td class='lable'>&nbsp;</td>
               <td class='input'><input type='submit' value='Generate' ></td>
              </tr>
              <tr>
               <td class='lable'>&nbsp;</td>
               <td class='input'><a href='./index.php?persons=2&amp;objects=4%3B5&amp;lengths=4%3B5%3B6&amp;max=4&amp;passesmin=1&amp;passesmax=4&amp;jugglerdoes=3+%283p+or+4p%29+or+3+%3Fp&amp;exclude=0+and+1+1+and+2+2&amp;clubdoes=%281+or+2%29+%281p+or+1.5p%29+or+%281p+or+1.5p%29+%281+or+2%29&amp;react=2p+3+or+4p+4+or+3+1.5p&amp;results=42&amp;doku=on'>documented example</a></td>
              </tr>
              <tr>
               <td class='lable'>&nbsp;</td>
               <td class='input'><a href='https://juggle.fandom.com/wiki/Prechac_patterns'>Prechac patterns (Juggle Wiki)</a></td>
              </tr>
             </table>
             $hidden_debug
            </form>
            ";
    
		 } 

        function correctPasses($passes){
            if (!is_numeric($passes)){
                return "_"; // pass to prolog as unspecified.
            }
            return $passes;
        }


        function doku($doku_flag){
        if ($doku_flag){
        $doku["head"]     = "   <td class='head'>Meaning</td>\n";
        $doku["persons"]  = "   <td class='sample'>2 persons</td>\n";
        $doku["objects"]  = "   <td class='sample'>4 or 5 objects</td>\n";
        $doku["length"]   = "   <td class='sample'>period length 4, 5 or 6.</td>\n";
        $doku["max"]      = "   <td class='sample'>highest throw is a 4</td>\n";
        $doku["multiplex"]= "   <td class='sample'>no multiplexes</td>\n";
        $doku["exclude"]  = "   <td class='sample'>exclude patterns that contain<br>a 0, a 1 1 or a 2 2</td>\n";
        $doku["contain"]  = "   <td class='sample'>find patterns that contain<br>3 3p or 3 4p or 3 followed by a pass.</td>\n";
        $doku["clubdoes"] = "   <td class='sample'>a club does a 1 or a 2 followed by a 1p or a 1.5p<br>or the other way round.</td>\n";
        $doku["react"]    = "   <td class='sample'>throw a 3 underneath an arriving 2p<br>or before catching a 4p throw a 4<br>or react with a 1.5p to a 3.</td>\n";
        $doku["results"]  = "   <td class='sample'>don't show more than 42 results.</td>\n";
        }else{$doku="";}
        return $doku;
        }


        // i'm not sure about the role of the line below, probably could be deleted (havarpan Feb 27 2024)
echo "<div id='path'>" . strstr($_SERVER["SCRIPT_FILENAME"], "/prechacthis/") ."</div>";
echo <<<EOD
</body>
</html>
EOD;
?>


