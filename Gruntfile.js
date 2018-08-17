module.exports = function (grunt) {

    require('load-grunt-tasks')(grunt);

    grunt.initConfig({
        pkg           : grunt.file.readJSON('package.json'),
        clean         : {
            all: ['build/*', 'respec/index.html']
        },
        replace       : {
            spec: {
                options: {
                    usePrefix: false,
                    patterns : [
                        {
                            match      : /%\s*(.*)/g,
                            replacement: ''
                        },
                        {
                            match      : /{{(.*)}}/g,
                            replacement: '{{@@include(\'$1\')}}'
                        },
                        {
                            match      : '<CODE BEGINS>',
                            replacement: ''
                        },
                        {
                            match      : '<CODE ENDS>',
                            replacement: ''
                        },
                        {
                            match      : '{mainmatter}',
                            replacement: ''
                        },
                        {
                            match      : '{backmatter}',
                            replacement: ''
                        },
                        {
                            match      : '.# Abstract',
                            replacement: ''
                        }
                    ]
                },
                files  : [
                    { expand: true, flatten: false, src: ['rfc/**/*.md'], dest: 'build/' }
                ]
            },
            dev : {
                options: {
                    usePrefix: false,
                    patterns : [
                        {
                            match      : '<script src="//localhost:35729/livereload.js"></script>',
                            replacement: ''
                        }
                    ]
                },
                files  : [
                    { src: 'respec/footer.html', dest: 'build/footer.html' }
                ]
            }
        },
        includereplace: {
            spec: {
                options: {
                    prefix     : '{{@@',
                    suffix     : '}}',
                    includesDir: 'build/'
                },
                files  : [
                    {
                        expand : true,
                        flatten: true,
                        src    : ['build/rfc/draft-oberstet-hybi-crossbar-wamp.md'],
                        dest   : 'build/'
                    }
                ]
            }
        },
        copy          : {
            spec: {
                options: {
                    process: (content, srcpath) => {
                        return content
                            .replace(/{align="left"}\n(\s+,((.|\n)*?)')\n\n/gm, '<pre>\n$1\n</pre>\n\n')
                            .replace(/{align="left"}\n(\s+\+((.|\n)*?)\+)\n\n/gm, '<pre>\n$1\n</pre>\n\n')
                            .replace(/{align="left"}\n(\|(.|\n)*?)(?=\n\n)/gm, '<pre>\n$1\n</pre>\n\n')
                            .replace(/{align="left"}\n((.|\n)*?)(?=\n\n[^\s])/gm, '```\n$1\n```\n\n')
                            .replace(/```\n```/g, '```')
                            .replace(/\n\n\n\n/gm, '\n\n');
                    }
                },
                files  : [
                    { src: 'build/draft-oberstet-hybi-crossbar-wamp.md', dest: 'build/spec.md' }
                ]
            }
        },
        concat        : {
            concatProd: {
                src : [
                    'respec/header.html',
                    'build/spec.md',
                    'build/footer.html'
                ],
                dest: 'respec/index.html'
            },
            concatDev : {
                src : [
                    'respec/header.html',
                    'build/spec.md',
                    'respec/footer.html'
                ],
                dest: 'respec/index.html'
            }
        },
        watch         : {
            sources: {
                files  : ['Gruntfile.js', 'respec/header.html', 'respec/footer.html', 'rfc/**/*.md'],
                tasks  : ['clean', 'replace:spec', 'includereplace', 'copy', 'concat:concatDev'],
                options: {
                    reload    : true,
                    livereload: true
                }
            }
        }
    });

    grunt.registerTask('default', ['clean', 'replace', 'includereplace', 'copy', 'concat:concatProd']);
};
