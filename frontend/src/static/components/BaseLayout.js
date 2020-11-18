import React from 'react';
import Navbar from 'react-bootstrap/Navbar';
import '../css/App.css';
import Container from 'react-bootstrap/Container';
import Fab from '@material-ui/core/Fab';
import AddIcon from '@material-ui/icons/Add';

class BaseLayout extends React.Component{
    constructor(props){
        super(props);
        this.navbar = !props.navbarDisabled ? this.createNavBar(props) : null ;
        this.container = <Container fluid={true}>{props.children}</Container>;
        this.fab = !props.fabDisabled ? this.createFab(props) : null ;
    }

    createNavBar(props){
        let _c = [];
        if(!props.menuBarDisabled){
            _c.unshift(<div>MENU BAR PLACE HOLDER</div>);
        }

        _c = props.navbarchildren ? _c.concat(props.navbarchildren) : _c; 

        return <Navbar expand={true} fixed='top' bg="dark" variant="dark">
                    {Object.keys(_c).map(
                        function (key) {
                            return <div key={key} className="Navbar-child">{_c[key]}</div>;
                        }
                    )}
                </Navbar>;
    }

    createFab(props){
        let positionClass = 'app-fab';

        if(props.fab_location && (props.fab_location === 'top-right' || props.fab_location === 'top')){
            positionClass += ' top-right';
        }
        else if(props.fab_location && props.fab_location === 'bottom-left'){
            positionClass += ' bottom-left';
        }
        else if(props.fab_location && props.fab_location === 'top-left'){
            positionClass += 'top-left';
        }
        else {
            positionClass += ' bottom-right';
        }

        let icon = props.fabIcon ? props.fabIcon : <AddIcon /> ;
        let label = props.fabLabel ? props.fabLabel : "add" ;
        let color = props.fabColor ? props.fabColor : "primary" ;
        let onClick = props.fabOnClick ? props.fabOnClick : null;
        return  <Fab color={color} aria-label={label} className={positionClass} onClick={onClick}>
                    {icon}
                </Fab>;
    }


    render(){
        return(
            <div className="h-100 w-100 d-flex">
                {this.navbar}
                {this.container}
                {this.fab}
            </div>
        );
    }
}

export default BaseLayout;