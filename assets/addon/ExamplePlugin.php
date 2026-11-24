<?php

namespace addon\example_plugin;

class ExamplePlugin extends \app\common\lib\Plugin
{
    public $info = [
        'name' => 'ExamplePlugin',
        'title' => '示例插件',
        'description' => '填写首版插件的用途',
        'author' => '填写作者',
        'version' => '0.0.0',
    ];

    public function install()
    {
        return true;
    }

    public function uninstall()
    {
        return true;
    }
}
